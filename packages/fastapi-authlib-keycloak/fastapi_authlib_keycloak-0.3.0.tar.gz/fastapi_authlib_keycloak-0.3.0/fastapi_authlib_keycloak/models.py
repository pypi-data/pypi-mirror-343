
from pydantic import BaseModel, Field, HttpUrl, PrivateAttr # Import PrivateAttr
from typing import Optional, List, Dict, Any, Union
from enum import Enum

class DiagnosticStatus(str, Enum):
    OK = "OK"
    ERROR = "ERROR"
    DISABLED = "DISABLED"

class ConnectionStatus(BaseModel):
    endpoint_url: Optional[str] = None
    status: DiagnosticStatus = DiagnosticStatus.OK
    message: Optional[str] = None
    latency_ms: Optional[float] = None
    cert_valid: Optional[bool] = None
    cert_expiry_days_remaining: Optional[int] = None
    cert_error_details: Optional[str] = None
    
class KeycloakDiagnosticResult(BaseModel):
    server_url: str
    realm: str
    ssl_verification_enabled: bool
    oidc_discovery_status: ConnectionStatus
    jwks_uri_status: ConnectionStatus
    introspection_endpoint_status: Optional[ConnectionStatus] = None 
    token_endpoint_status: Optional[ConnectionStatus] = None 


class IntrospectionResult(BaseModel):
    """Model for the response from Keycloak's token introspection endpoint."""
    active: bool
    sub: Optional[str] = None
    # Changed alias back to "username" to potentially match other sources if needed,
    # but kept the field name as "username" for consistency.
    username: Optional[str] = Field(None, alias="username") 
    preferred_username: Optional[str] = Field(None) # Add explicit field for preferred_username
    email: Optional[str] = None
    client_id: Optional[str] = None
    token_type: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None
    nbf: Optional[int] = None
    iss: Optional[str] = None
    aud: Optional[Union[str, List[str]]] = None
    realm_access: Optional[Dict[str, List[str]]] = None
    resource_access: Optional[Dict[str, Dict[str, List[str]]]] = None
    scope: Optional[str] = None
    groups: Optional[List[str]] = None
    
    # Use PrivateAttr for internal storage, not part of the model fields
    _raw_data: Dict[str, Any] = PrivateAttr(default_factory=dict)
    
    # Override __init__ to capture raw data before validation
    def __init__(self, **data: Any):
        self._raw_data = data.copy() # Capture raw data into the private attribute
        super().__init__(**data)
        
    class Config:
        extra = 'allow' # Allow extra fields from Keycloak not explicitly defined
        populate_by_name = True # Allow alias usage like preferred_username

class KeycloakUser(BaseModel):
    """Represents the authenticated user and their claims."""
    sub: str = Field(...)
    # Changed alias from preferred_username back to username for consistency
    # This field will now be populated by the 'username' claim if present,
    # or fallback to 'preferred_username' in from_token/from_introspection.
    username: Optional[str] = Field(None, alias="username") 
    preferred_username: Optional[str] = Field(None) # Keep explicit preferred_username
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    roles: List[str] = Field([])
    groups: List[str] = Field([])
    raw_claims: Dict[str, Any] = Field({})
    
    @classmethod
    def _extract_roles(cls, data: Dict[str, Any]) -> List[str]:
        realm = data.get("realm_access", {}).get("roles", []) if isinstance(data.get("realm_access"), dict) else []
        client = []
        res = data.get("resource_access", {})
        if isinstance(res, dict): 
             for c in res.values(): client.extend(c.get("roles", []) if isinstance(c, dict) else [])
        return list(set(realm + client))
        
    @classmethod
    def from_token(cls, payload: Dict[str, Any]) -> 'KeycloakUser':
        roles = cls._extract_roles(payload); groups = payload.get("groups", [])
        # Prioritize 'username' claim, fallback to 'preferred_username'
        username_value = payload.get("username") or payload.get("preferred_username")
        data = {
            "sub": payload.get("sub"), 
            "username": username_value, 
            "preferred_username": payload.get("preferred_username"), # Still store preferred_username if present
            "email": payload.get("email"), 
            "email_verified": payload.get("email_verified"), 
            "given_name": payload.get("given_name"), 
            "family_name": payload.get("family_name"), 
            "name": payload.get("name")
        }
        data["roles"] = roles; data["groups"] = groups if isinstance(groups, list) else []; data["raw_claims"] = payload
        filtered = {k: v for k, v in data.items() if v is not None}
        if "sub" not in filtered: raise ValueError("Missing 'sub' claim")
        return cls(**filtered)
        
    @classmethod
    def from_introspection(cls, intro: 'IntrospectionResult') -> 'KeycloakUser':
        if not intro.active or not intro.sub: raise ValueError("Inactive/sub-less introspection result")
        # Access the raw data from the private attribute
        raw = intro._raw_data 
        roles = cls._extract_roles(raw); groups = raw.get("groups", [])
        # Prioritize 'username' claim, fallback to 'preferred_username'
        username_value = raw.get("username") or raw.get("preferred_username")
        data = {
            "sub": intro.sub, 
            "username": username_value, 
            "preferred_username": raw.get("preferred_username"), # Store preferred_username if present
            "email": intro.email,
            "email_verified": raw.get("email_verified"), 
            "given_name": raw.get("given_name"),
            "family_name": raw.get("family_name"), 
            "name": raw.get("name"),
            "roles": roles, 
            "groups": groups if isinstance(groups, list) else [], 
            "raw_claims": raw
        }
        return cls(**{k: v for k, v in data.items() if v is not None})

class TokenResponse(BaseModel):
    access_token: str; expires_in: int; refresh_expires_in: Optional[int] = None
    refresh_token: Optional[str] = None; token_type: str; id_token: Optional[str] = None
    not_before_policy: Optional[int] = Field(None, alias="not-before-policy")
    session_state: Optional[str] = None; scope: Optional[str] = None
    class Config: extra = 'allow'; populate_by_name = True
