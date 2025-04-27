
import logging
from typing import Optional, Set, TYPE_CHECKING # Import TYPE_CHECKING
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp # Import ASGIApp

# Import KeycloakManager only under TYPE_CHECKING
# from .builder import KeycloakManager # Remove direct import
from .errors import AuthError, NoAuthorizationHeaderError, InvalidAuthorizationHeaderError
from .models import KeycloakUser

# Use TYPE_CHECKING block for imports causing cycles
if TYPE_CHECKING:
    from .builder import KeycloakManager 

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    """
    FastAPI Middleware to handle token authentication via KeycloakManager.
    Extracts bearer token, calls manager.authenticate_token(), and attaches user info to request.state.
    """
    # Use string forward reference for KeycloakManager type hint
    # Accept 'app' as the first argument
    def __init__(self, app: ASGIApp, manager: 'KeycloakManager', public_paths: Optional[Set[str]] = None):
        """
        Args:
            app: The ASGI application instance.
            manager: An initialized KeycloakManager instance.
            public_paths: A set of URL paths (or path prefixes) that should bypass authentication.
        """
        # Pass 'app' to super().__init__()
        super().__init__(app) 
        self.manager = manager
        self.public_paths = public_paths or set()
        logger.info(f"AuthMiddleware initialized. Public paths: {self.public_paths or 'None'}")

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Check if path is public
        if request.url.path in self.public_paths or any(request.url.path.startswith(p) for p in self.public_paths if p.endswith('/')) :
            logger.debug(f"Request path {request.url.path} is public, skipping auth.")
            request.state.user = None
            return await call_next(request)

        # Extract token
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            error = NoAuthorizationHeaderError()
            logger.warning(f"Missing Auth header: {request.url.path}")
            return JSONResponse(status_code=error.status_code, content=error.detail)

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            error = InvalidAuthorizationHeaderError()
            logger.warning(f"Invalid Auth header format: {request.url.path}")
            return JSONResponse(status_code=error.status_code, content=error.detail)
            
        token = parts[1]

        # Authenticate token using the manager
        try:
            user: KeycloakUser = await self.manager.authenticate_token(token)
            request.state.user = user
            logger.debug(f"User {user.sub} authenticated: {request.url.path}")
        except AuthError as err:
            logger.warning(f"Auth failed: {err.code} - {err.message} ({request.url.path})")
            return JSONResponse(status_code=err.status_code, content=err.detail)
        except Exception as e:
            logger.error(f"Unexpected auth error: {e} ({request.url.path})", exc_info=True)
            internal_error = AuthError(status_code=500, code="internal_server_error", message="Unexpected auth error.")
            return JSONResponse(status_code=internal_error.status_code, content=internal_error.detail)
            
        # Proceed to the endpoint
        response = await call_next(request)
        return response
