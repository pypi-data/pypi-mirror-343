
import pytest
import time
import json # Import json for alg=none test
import base64 # Import base64 for alg=none test
import jwt 
from freezegun import freeze_time

from fastapi_authlib_keycloak import (
    TokenValidator, KeycloakAdapter, KeycloakConfig, KeycloakUser,
    InvalidTokenError, InvalidSignatureError, TokenExpiredError, InvalidClaimsError,
    MissingClaimError, UnknownKidError, InvalidAlgorithmError
)

from .conftest import create_test_token, MOCK_CLIENT_ID, MOCK_ISSUER 

@pytest.fixture
def token_validator(keycloak_config: KeycloakConfig, keycloak_adapter: KeycloakAdapter) -> TokenValidator:
    return TokenValidator(config=keycloak_config, adapter=keycloak_adapter)

@pytest.mark.asyncio
async def test_validate_valid_token(token_validator: TokenValidator, test_rsa_key_pair: dict):
    token = create_test_token(test_rsa_key_pair)
    user = await token_validator.validate_token(token)
    assert isinstance(user, KeycloakUser)
    assert user.sub == "test-subject"
    assert user.username == "testuser"

@pytest.mark.asyncio
@freeze_time("2023-01-01 12:00:00")
async def test_validate_expired_token(token_validator: TokenValidator, test_rsa_key_pair: dict):
    token = create_test_token(test_rsa_key_pair, expiry_delta_seconds=-60)
    with pytest.raises(TokenExpiredError):
        await token_validator.validate_token(token)

# Freeze time slightly *before* the default nbf time (which is token creation time)
@pytest.mark.asyncio
@freeze_time("2023-01-01 11:59:59") 
async def test_validate_immature_token(token_validator: TokenValidator, test_rsa_key_pair: dict):
    # Freeze time slightly *after* the nbf check to ensure it's evaluated
    with freeze_time("2023-01-01 12:00:00"):
      token = create_test_token(test_rsa_key_pair) # nbf = 12:00:00
    # Now validate when current time is 11:59:59
    with pytest.raises(InvalidClaimsError) as excinfo:
        await token_validator.validate_token(token)
    assert excinfo.value.code == "invalid_claims"
    assert excinfo.value.details.get("claim") == "nbf"

@pytest.mark.asyncio
async def test_validate_invalid_signature(token_validator: TokenValidator, test_rsa_key_pair: dict):
    token = create_test_token(test_rsa_key_pair)
    parts = token.split('.'); tampered_token = f"{parts[0]}.{parts[1]}.{parts[2][:-5]}abcde"
    with pytest.raises(InvalidSignatureError):
        await token_validator.validate_token(tampered_token)

@pytest.mark.asyncio
async def test_validate_incorrect_issuer(token_validator: TokenValidator, test_rsa_key_pair: dict, keycloak_config: KeycloakConfig):
    keycloak_config.issuer = "https://correct-issuer.test"
    validator_with_issuer = TokenValidator(config=keycloak_config, adapter=token_validator.adapter)
    token = create_test_token(test_rsa_key_pair, issuer="https://wrong-issuer.test")
    with pytest.raises(InvalidClaimsError) as excinfo:
        await validator_with_issuer.validate_token(token)
    assert excinfo.value.code == "invalid_claims"; assert excinfo.value.details.get("claim") == "iss"

@pytest.mark.asyncio
async def test_validate_incorrect_audience(token_validator: TokenValidator, test_rsa_key_pair: dict, keycloak_config: KeycloakConfig):
    keycloak_config.audience = "expected-audience"
    validator_with_aud = TokenValidator(config=keycloak_config, adapter=token_validator.adapter)
    token = create_test_token(test_rsa_key_pair, audience="actual-audience")
    with pytest.raises(InvalidClaimsError) as excinfo:
        await validator_with_aud.validate_token(token)
    assert excinfo.value.code == "invalid_claims"; assert excinfo.value.details.get("claim") == "aud"

@pytest.mark.asyncio
async def test_validate_missing_kid(token_validator: TokenValidator, test_rsa_key_pair: dict):
    # Explicitly set kid to None in headers_override to ensure it's removed
    token = create_test_token(test_rsa_key_pair, headers_override={"alg": "RS256", "kid": None})
    # Add assertion to check header parsing
    unverified_header = jwt.get_unverified_header(token)
    assert "kid" not in unverified_header
    with pytest.raises(UnknownKidError) as excinfo:
         await token_validator.validate_token(token)
    assert excinfo.value.details.get("kid") == "<missing>"

@pytest.mark.asyncio
async def test_validate_unknown_kid(token_validator: TokenValidator, test_rsa_key_pair: dict, respx_router):
    original_get_jwk = token_validator.adapter.get_jwk_for_kid
    async def mock_get_jwk_for_kid(kid: str):
        if kid == "unknown-kid": return None
        return await original_get_jwk(kid) 
    token_validator.adapter.get_jwk_for_kid = mock_get_jwk_for_kid
    token = create_test_token(test_rsa_key_pair, headers_override={"kid": "unknown-kid"})
    with pytest.raises(UnknownKidError) as excinfo:
        await token_validator.validate_token(token)
    assert excinfo.value.details.get("kid") == "unknown-kid"
    token_validator.adapter.get_jwk_for_kid = original_get_jwk

@pytest.mark.asyncio
async def test_validate_alg_none_rejected(token_validator: TokenValidator, test_rsa_key_pair: dict):
    headers = {"alg": "none", "kid": test_rsa_key_pair["jwk"]["kid"]}
    payload = {"sub": "test"}
    # Use standard json + base64
    json_header = json.dumps(headers, separators=(",", ":")).encode('utf-8')
    json_payload = json.dumps(payload, separators=(",", ":")).encode('utf-8')
    token_parts = [
        base64.urlsafe_b64encode(json_header).rstrip(b'=').decode('ascii'),
        base64.urlsafe_b64encode(json_payload).rstrip(b'=').decode('ascii'),
        "" 
    ]
    none_token = ".".join(token_parts)
    with pytest.raises(InvalidAlgorithmError) as excinfo:
        await token_validator.validate_token(none_token)
    assert excinfo.value.details.get("algorithm") == "none"

@pytest.mark.asyncio
async def test_validate_disallowed_alg(token_validator: TokenValidator, test_rsa_key_pair: dict, keycloak_config: KeycloakConfig):
    keycloak_config.algorithms = ["RS512"]
    validator_strict_alg = TokenValidator(config=keycloak_config, adapter=token_validator.adapter)
    token = create_test_token(test_rsa_key_pair)
    with pytest.raises(InvalidAlgorithmError) as excinfo:
        await validator_strict_alg.validate_token(token)
    assert excinfo.value.details.get("algorithm") == "RS256"

