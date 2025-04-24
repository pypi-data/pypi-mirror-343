
from fastapi import HTTPException, status
from typing import Optional, Dict, Any, List # Added List

class AuthError(HTTPException):
    """Base class for authentication and authorization errors in this library."""
    def __init__(self, status_code: int, code: str, message: str, details: Optional[Dict[str, Any]] = None):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or {}
        error_payload = {
            "error": {
                "code": self.code,
                "message": self.message
            }
        }
        if self.details:
            error_payload["error"]["details"] = self.details
        super().__init__(status_code=self.status_code, detail=error_payload)

# --- JWT Validation Errors --- 

class InvalidTokenError(AuthError):
    def __init__(self, message: str = "Malformed authorization token", details: Optional[Dict[str, Any]] = None):
        super().__init__(status.HTTP_400_BAD_REQUEST, "malformed_token", message, details)

class InvalidSignatureError(AuthError):
    def __init__(self, message: str = "Token signature verification failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "invalid_signature", message, details)

class TokenExpiredError(AuthError):
    def __init__(self, message: str = "Token has expired", expiry: Optional[int] = None):
        details = {"expiry": expiry} if expiry else None
        super().__init__(status.HTTP_401_UNAUTHORIZED, "token_expired", message, details)

class InvalidClaimsError(AuthError):
    def __init__(self, claim: str, message: str = "Invalid token claims", details: Optional[Dict[str, Any]] = None):
        base_details = {"claim": claim}
        if details:
            base_details.update(details)
        super().__init__(status.HTTP_401_UNAUTHORIZED, "invalid_claims", message, base_details)

class MissingClaimError(AuthError):
    def __init__(self, claim: str, message: str = "Missing required claim"):
        details = {"claim": claim}
        super().__init__(status.HTTP_401_UNAUTHORIZED, "missing_claim", message, details)
        
class UnknownKidError(AuthError):
    def __init__(self, kid: str, message: str = "Unknown Key ID (kid) in token header"):
        details = {"kid": kid}
        super().__init__(status.HTTP_401_UNAUTHORIZED, "unknown_kid", message, details)
        
class InvalidAlgorithmError(AuthError):
    def __init__(self, algorithm: str, message: str = "Invalid or unsupported algorithm in token"):
        details = {"algorithm": algorithm}
        super().__init__(status.HTTP_401_UNAUTHORIZED, "invalid_algorithm", message, details)

# --- Introspection Errors --- 

class IntrospectionError(AuthError):
    def __init__(self, status_code: int, code: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, code, message, details)

class TokenInactiveError(IntrospectionError):
    def __init__(self, message: str = "Token is inactive or revoked", details: Optional[Dict[str, Any]] = None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "token_inactive", message, details)

class IntrospectionServiceError(IntrospectionError):
    def __init__(self, status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE, code: str = "introspection_service_error", message: str = "Error communicating with introspection service", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, code, message, details)

# --- Token Refresh Errors --- Added Section

class TokenRefreshError(AuthError):
    """Error during token refresh attempt."""
    def __init__(self, status_code: int = status.HTTP_400_BAD_REQUEST, code: str = "token_refresh_failed", message: str = "Failed to refresh token", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, code, message, details)

# --- Keycloak Communication/Configuration Errors --- 

class KeycloakConfigurationError(AuthError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, "keycloak_config_error", message, details)

class KeycloakConnectionError(AuthError):
    def __init__(self, code: str = "keycloak_connection_error", message: str = "Could not connect to Keycloak", details: Optional[Dict[str, Any]] = None):
        super().__init__(status.HTTP_503_SERVICE_UNAVAILABLE, code, message, details)
        
class CertError(KeycloakConnectionError):
     def __init__(self, code: str, message: str, details: Optional[Dict[str, Any]] = None):
         super().__init__(code, message, details)

class CertExpiredError(CertError):
    def __init__(self, message: str = "Keycloak server certificate has expired", details: Optional[Dict[str, Any]] = None):
        super().__init__("cert_expired", message, details)

class CertUntrustedError(CertError):
    def __init__(self, message: str = "Keycloak server certificate is not trusted", details: Optional[Dict[str, Any]] = None):
        super().__init__("cert_untrusted", message, details)
        
class HostnameMismatchError(CertError):
    def __init__(self, message: str = "Keycloak server hostname mismatch", details: Optional[Dict[str, Any]] = None):
        super().__init__("hostname_mismatch", message, details)

# --- Authorization Errors --- 

class AuthorizationError(AuthError):
    def __init__(self, status_code: int = status.HTTP_403_FORBIDDEN, code: str = "forbidden", message: str = "Permission denied", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code, code, message, details)

class MissingRolesError(AuthorizationError):
    def __init__(self, required_roles: List[str], user_roles: List[str]):
        details = {"required_roles": required_roles, "user_roles": user_roles}
        message = f"User is missing required roles: {required_roles}"
        super().__init__(status.HTTP_403_FORBIDDEN, "missing_roles", message, details)

class MissingGroupsError(AuthorizationError):
    def __init__(self, required_groups: List[str], user_groups: List[str]):
        details = {"required_groups": required_groups, "user_groups": user_groups}
        message = f"User is missing required group membership: {required_groups}"
        super().__init__(status.HTTP_403_FORBIDDEN, "missing_groups", message, details)
        
# --- Dependency Errors ---

class NoAuthenticatedUserError(AuthError):
    """Error raised by dependencies when no authenticated user is found in request.state."""
    def __init__(self, message: str = "Authenticated user not found in request state."):
        # This typically indicates a logic error (middleware didn't run or failed silently)
        # or the dependency was used on a public route without proper checks.
        super().__init__(status.HTTP_401_UNAUTHORIZED, "not_authenticated", message)

# --- Other Errors ---

class NoAuthorizationHeaderError(AuthError):
    def __init__(self, message: str = "Authorization header is missing"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "missing_header", message)

class InvalidAuthorizationHeaderError(AuthError):
    def __init__(self, message: str = "Invalid Authorization header format. Expected 'Bearer <token>'"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "invalid_header_format", message)

