
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Union, List # Import List

class KeycloakConfig(BaseModel):
    """Keycloak Configuration Model"""
    server_url: HttpUrl = Field(..., description="URL of the Keycloak server (e.g., 'https://localhost:8443')")
    realm: str = Field(..., description="Keycloak realm name")
    client_id: str = Field(..., description="Client ID for this application")
    client_secret: Optional[str] = Field(None, description="Client secret (required for confidential clients)")
    
    # Endpoints (can often be derived from server_url/realm)
    well_known_endpoint: Optional[HttpUrl] = Field(None, description="Override for the OIDC well-known configuration endpoint")
    jwks_uri: Optional[HttpUrl] = Field(None, description="Override for the JWKS URI")
    introspection_endpoint: Optional[HttpUrl] = Field(None, description="Override for the token introspection endpoint")
    token_endpoint: Optional[HttpUrl] = Field(None, description="Override for the token endpoint (for refresh)")
    
    # Validation settings
    # Use typing.List for Python 3.8 compatibility
    audience: Optional[Union[str, List[str]]] = Field(None, description="Expected audience ('aud' claim)")
    issuer: Optional[Union[str, List[str]]] = Field(None, description="Expected issuer ('iss' claim)")
    algorithms: List[str] = Field(["RS256"], description="Allowed JWT signing algorithms")
    
    # Caching
    cache_maxsize: int = Field(128, description="Maximum size for in-memory LRU cache for JWKS keys")
    cache_ttl: int = Field(3600, description="Time-to-live in seconds for cached JWKS keys")
    
    # HTTP Client Settings
    connect_timeout: int = Field(5, description="Connection timeout in seconds for HTTP requests to Keycloak")
    read_timeout: int = Field(5, description="Read timeout in seconds for HTTP requests to Keycloak")
    verify_ssl: bool = Field(True, description="Verify SSL certificates for Keycloak connections")
    
    # Features
    use_introspection: bool = Field(False, description="Use token introspection endpoint instead of local JWT validation (requires client_secret)")
    enable_refresh: bool = Field(False, description="Enable automatic token refresh (requires client_secret)")
    
    # Internal usage: derived endpoints
    _derived_well_known_endpoint: Optional[HttpUrl] = None
    _derived_jwks_uri: Optional[HttpUrl] = None
    _derived_introspection_endpoint: Optional[HttpUrl] = None
    _derived_token_endpoint: Optional[HttpUrl] = None

    def get_well_known_endpoint(self) -> str:
        if self.well_known_endpoint:
            return str(self.well_known_endpoint)
        if self._derived_well_known_endpoint:
            return str(self._derived_well_known_endpoint)
        # Construct default if not provided or derived yet
        return f"{str(self.server_url).rstrip('/')}/realms/{self.realm}/.well-known/openid-configuration"
        
    def get_jwks_uri(self) -> Optional[str]:
        if self.jwks_uri:
            return str(self.jwks_uri)
        return str(self._derived_jwks_uri) if self._derived_jwks_uri else None

    def get_introspection_endpoint(self) -> Optional[str]:
        if self.introspection_endpoint:
            return str(self.introspection_endpoint)
        return str(self._derived_introspection_endpoint) if self._derived_introspection_endpoint else None
        
    def get_token_endpoint(self) -> Optional[str]:
        if self.token_endpoint:
            return str(self.token_endpoint)
        return str(self._derived_token_endpoint) if self._derived_token_endpoint else None

    class Config:
        validate_assignment = True # Ensure derived fields are validated if set later
