
"""FastAPI Keycloak Integration - Opinionated authentication and authorization based on Keycloak.

Provides utilities for integrating FastAPI applications with Keycloak for authentication
and authorization, handling JWT validation, introspection, roles, and more.
"""

__version__ = "0.3.6"

import logging

# --- Core Configuration and Models ---
from .config import KeycloakConfig
from .models import (
    KeycloakUser,
    TokenResponse,
    IntrospectionResult,
    KeycloakDiagnosticResult,
    ConnectionStatus,
    DiagnosticStatus,
)

# --- Main Integration Components ---
from .builder import KeycloakBuilder, KeycloakManager
from .middleware import AuthMiddleware

# --- Dependencies for Route Protection ---
from .dependencies import get_current_user, require_roles, require_groups, RoleChecker, GroupChecker

# --- Errors --- #
# Import all specific error types users might want to catch
from .errors import (
    AuthError,
    # JWT Errors
    InvalidTokenError,
    InvalidSignatureError,
    TokenExpiredError,
    InvalidClaimsError,
    MissingClaimError,
    UnknownKidError,
    InvalidAlgorithmError,
    # Introspection Errors
    IntrospectionError,
    TokenInactiveError,
    IntrospectionServiceError,
    # Refresh Errors
    TokenRefreshError,
    # Communication/Config Errors
    KeycloakConfigurationError,
    KeycloakConnectionError,
    CertError,
    CertExpiredError,
    CertUntrustedError,
    HostnameMismatchError,
    # Authorization Errors
    AuthorizationError,
    MissingRolesError,
    MissingGroupsError,
    # Header Errors
    NoAuthorizationHeaderError,
    InvalidAuthorizationHeaderError,
)

# --- Optional Components (Users might import these for type hinting or direct use) ---
from .adapter import KeycloakAdapter
from .validator import TokenValidator
from .client import IntrospectionClient
from .refresh import RefreshManager
from .metrics import MetricsCollector, NoOpMetricsCollector # For custom implementations


# --- Define Public API Surface --- #
__all__ = [
    # Setup & Management
    "KeycloakBuilder",
    "KeycloakManager",
    # Config & Models
    "KeycloakConfig",
    "KeycloakUser",
    "TokenResponse",
    "IntrospectionResult",
    "KeycloakDiagnosticResult",
    "ConnectionStatus",
    "DiagnosticStatus",
    # Middleware
    "AuthMiddleware",
    # Dependencies
    "get_current_user",
    "require_roles",
    "require_groups",
    "RoleChecker", # Expose checker classes too
    "GroupChecker",
    # Errors (Expose all imported errors)
    "AuthError",
    "InvalidTokenError",
    "InvalidSignatureError",
    "TokenExpiredError",
    "InvalidClaimsError",
    "MissingClaimError",
    "UnknownKidError",
    "InvalidAlgorithmError",
    "IntrospectionError",
    "TokenInactiveError",
    "IntrospectionServiceError",
    "TokenRefreshError",
    "KeycloakConfigurationError",
    "KeycloakConnectionError",
    "CertError",
    "CertExpiredError",
    "CertUntrustedError",
    "HostnameMismatchError",
    "AuthorizationError",
    "MissingRolesError",
    "MissingGroupsError",
    "NoAuthorizationHeaderError",
    "InvalidAuthorizationHeaderError",
    # Lower-level components (Optional)
    "KeycloakAdapter",
    "TokenValidator",
    "IntrospectionClient",
    "RefreshManager",
    # Metrics (for implementers)
    "MetricsCollector",
    "NoOpMetricsCollector",
]

# Configure basic logging to avoid "No handler found" warnings
logging.getLogger(__name__).addHandler(logging.NullHandler())
