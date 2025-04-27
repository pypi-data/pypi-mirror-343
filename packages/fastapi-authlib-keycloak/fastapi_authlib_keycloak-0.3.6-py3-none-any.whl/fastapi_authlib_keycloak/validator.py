
import jwt # PyJWT library
import logging
import time
from typing import Dict, Any, Optional

from .config import KeycloakConfig
from .adapter import KeycloakAdapter
from .models import KeycloakUser
from .errors import (
    AuthError, InvalidTokenError, InvalidSignatureError, TokenExpiredError, 
    InvalidClaimsError, MissingClaimError, UnknownKidError,
    InvalidAlgorithmError, KeycloakConfigurationError
)
from .metrics import MetricsCollector, NoOpMetricsCollector

logger = logging.getLogger(__name__)

class TokenValidator:
    """Validates JWT tokens using PyJWT, Keycloak config, keys from Adapter, and collects metrics."""

    def __init__(self, config: KeycloakConfig, adapter: KeycloakAdapter, metrics: Optional[MetricsCollector] = None):
        self.config = config
        self.adapter = adapter
        self.metrics = metrics or NoOpMetricsCollector()
        logger.info("Token Validator initialized.")
        if "none" in [alg.lower() for alg in config.algorithms]:
            logger.critical("Config allows 'none' algorithm. Validator blocks it, but fix config.")

    def _get_public_key(self, jwk: Dict[str, Any], alg: str):
        try:
            algo_instance = jwt.get_algorithm_by_name(alg)
            return algo_instance.from_jwk(jwk)
        except jwt.UnsupportedAlgorithmError:
             logger.error(f"Algorithm '{alg}' unsupported by PyJWT.")
             raise InvalidAlgorithmError(algorithm=alg, message=f"Alg '{alg}' unsupported by JWT lib.")
        except Exception as e:
             logger.error(f"Failed to import public key from JWK for alg '{alg}': {e}", exc_info=True)
             raise KeycloakConfigurationError(f"Could not load pub key for alg '{alg}': {e}") from e

    async def validate_token(self, token: str, **kwargs) -> KeycloakUser:
        start_time = time.perf_counter()
        try:
            try:
                unverified_header = jwt.get_unverified_header(token)
            except jwt.DecodeError as e:
                raise InvalidTokenError(f"Could not decode JWT header: {e}") from e
                
            alg = unverified_header.get("alg")
            if not alg: raise InvalidAlgorithmError(algorithm="<missing>", message="Token header missing 'alg'")
            if alg.lower() == "none": 
                logger.critical("Rejected token using 'none' algorithm.")
                raise InvalidAlgorithmError(algorithm="none", message="'none' algorithm forbidden.")
            if alg not in self.config.algorithms: 
                raise InvalidAlgorithmError(algorithm=alg, message=f"Token alg '{alg}' not allowed by config: {self.config.algorithms}")

            kid = unverified_header.get("kid")
            # Ensure KID check happens *before* key fetch attempt
            if not kid: 
                logger.warning("Token header missing 'kid' field.") # Log for clarity
                raise UnknownKidError(kid="<missing>", message="Token header missing 'kid'")

            jwk = await self.adapter.get_jwk_for_kid(kid)
            if not jwk: 
                # Adapter already logs error if KID not found after refresh
                raise UnknownKidError(kid=kid, message=f"No public key found for kid '{kid}'.")
                
            public_key = self._get_public_key(jwk, alg)

            options = {
                "verify_signature": True, "verify_exp": True, "verify_nbf": True,
                "verify_iat": True, "verify_aud": self.config.audience is not None,
                "verify_iss": self.config.issuer is not None, "require": []
            }
            options.update(kwargs)
            
            payload = jwt.decode(
                token, public_key, algorithms=[alg], audience=self.config.audience,
                issuer=self.config.issuer, options=options
            )
            
            decode_verify_latency = (time.perf_counter() - start_time) * 1000
            logger.debug(f"JWT decode/verify took {decode_verify_latency:.2f} ms")
            
            user = KeycloakUser.from_token(payload)
            logger.info(f"Token validated successfully (JWT) for user: {user.username} (sub: {user.sub})")
            return user

        # --- Error Handling --- 
        except jwt.ExpiredSignatureError as e: raise TokenExpiredError(expiry=getattr(e, 'expiry', None)) from e
        except jwt.InvalidSignatureError as e: raise InvalidSignatureError() from e
        except jwt.MissingRequiredClaimError as e: raise MissingClaimError(claim=e.claim) from e
        except jwt.InvalidAudienceError as e: raise InvalidClaimsError(claim="aud", message=f"Invalid audience: {getattr(e, 'actual_audience', '<unknown>')}", details={"expected": self.config.audience, "actual": getattr(e, 'actual_audience', None)}) from e
        except jwt.InvalidIssuerError as e: raise InvalidClaimsError(claim="iss", message=f"Invalid issuer: {getattr(e, 'actual_issuer', '<unknown>')}", details={"expected": self.config.issuer, "actual": getattr(e, 'actual_issuer', None)}) from e
        except jwt.InvalidIssuedAtError as e: raise InvalidClaimsError(claim="iat", message=f"Invalid iat: {e}") from e
        # Corrected: Use ImmatureSignatureError for nbf check
        except jwt.ImmatureSignatureError as e: raise InvalidClaimsError(claim="nbf", message=f"Token not yet valid (nbf): {e}") from e 
        except jwt.InvalidAlgorithmError as e: raise InvalidAlgorithmError(algorithm=alg if 'alg' in locals() else '<unknown>', message=f"PyJWT rejected algorithm: {e}") from e
        except jwt.DecodeError as e: raise InvalidTokenError(f"Failed JWT decode/parse: {e}") from e
        except AuthError as e: raise e # Re-raise our specific errors
        except Exception as e:
            logger.error(f"Unexpected error during JWT validation: {e}", exc_info=True)
            raise AuthError(status_code=500, code="jwt_validation_unexpected_error", message=f"Unexpected JWT validation error: {e}") from e
