# FastAPI Authlib Keycloak Integration

[![PyPI version](https://badge.fury.io/py/fastapi-authlib-keycloak.svg?icon=si%3Apython)](https://badge.fury.io/py/fastapi-authlib-keycloak) [![Build Status](https://github.com/c0mpiler/fastapi-authlib-keycloak/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/c0mpiler/fastapi-authlib-keycloak/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/c0mpiler/fastapi-authlib-keycloak/graph/badge.svg?branch=main&token=5SDNYOB50Z)](https://codecov.io/gh/c0mpiler/fastapi-authlib-keycloak)

Provides robust and efficient Keycloak integration for FastAPI applications, handling common scenarios like JWT validation, token introspection, refresh tokens, role/group authorization, metrics, diagnostics, and OpenAPI integration.

## Features

*   **Fluent Configuration:** Easy setup using a `KeycloakBuilder`.
*   **JWT Validation:** Local validation of JWT access tokens using JWKS fetched from Keycloak.
*   **Token Introspection:** Optional validation via Keycloak's token introspection endpoint.
*   **Token Refresh:** Support for exchanging refresh tokens (requires a dedicated endpoint in your app).
*   **Authorization Dependencies:** FastAPI dependencies (`require_roles`, `require_groups`) for easy endpoint protection.
*   **Middleware:** Standard FastAPI middleware for automatic token extraction and validation.
*   **OpenAPI/Swagger Integration:** Helper for security scheme setup in interactive API documentation.
*   **Caching:** Configurable in-memory caching for Keycloak's OIDC discovery document and JWKS.
*   **Metrics:** Pluggable metrics collection interface (implement with Prometheus, etc.).
*   **TLS Diagnostics:** Helper function to test connectivity and certificate validity.
*   **Async Support:** Fully asynchronous using `httpx` and `asyncio`.

## Installation

```bash
pip install fastapi-authlib-keycloak
```

## Quick Start

```python
import logging
import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel # Needed for RefreshRequest
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from fastapi_authlib_keycloak import (
    KeycloakBuilder,
    KeycloakManager,
    KeycloakUser,
    require_roles,
    AuthError,
    KeycloakDiagnosticResult
)

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- Configuration (Use Environment Variables or Secrets Manager!) ---
KEYCLOAK_URL = "https://YOUR_KEYCLOAK_SERVER/auth/"
KEYCLOAK_REALM = "YOUR_REALM"
KEYCLOAK_CLIENT_ID = "your-fastapi-client-id"
KEYCLOAK_CLIENT_SECRET = "YOUR_CLIENT_SECRET"

# 1. Configure Keycloak Integration
keycloak_manager: KeycloakManager = KeycloakBuilder() \
    .with_server_url(KEYCLOAK_URL) \
    .with_realm(KEYCLOAK_REALM) \
    .with_client_id(KEYCLOAK_CLIENT_ID) \
    .with_client_secret(KEYCLOAK_CLIENT_SECRET) \
    .enable_token_refresh() \
    .with_openapi_security_scheme(
        scheme_name="KeycloakAuth (Implicit Flow)",
        scopes={"openid": "OpenID", "profile": "Profile", "email": "Email"}
    ) \
    .build()

# 2. Create FastAPI App
app = FastAPI(title="Keycloak Protected API")

# 3. Add Middleware
app.add_middleware(
    keycloak_manager.get_middleware(public_paths={"/docs", "/openapi.json", "/", "/health/keycloak"})
)

# 4. Add Exception Handler
@app.exception_handler(AuthError)
async def auth_error_handler(request, exc: AuthError):
    return JSONResponse(status_code=exc.status_code, content=exc.detail)

# 5. Configure OpenAPI Security
oauth2_scheme = None

@app.on_event("startup")
async def startup_event():
    global oauth2_scheme
    try:
        await keycloak_manager.adapter.get_oidc_config()
        oauth2_scheme = await keycloak_manager.get_security_scheme()
        logging.info("OpenAPI security scheme configured.")
    except Exception as e:
        logging.error(f"Could not configure OpenAPI security: {e}", exc_info=True)

def custom_openapi():
    if app.openapi_schema: return app.openapi_schema
    openapi_schema = get_openapi(title=app.title, version="1.0.0", routes=app.routes)
    if oauth2_scheme:
        scheme_name = keycloak_manager._openapi_scheme_name
        scopes = keycloak_manager._openapi_scopes or {}
        openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})[scheme_name] = oauth2_scheme.model
        openapi_schema["security"] = [{scheme_name: list(scopes.keys())}]
    else:
        logging.warning("OAuth2 scheme unavailable for OpenAPI.")
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# 6. Define Endpoints
@app.get("/")
async def root(): return {"message": "Public root"}

@app.get("/users/me", response_model=KeycloakUser)
async def get_me(user: KeycloakUser = Depends(keycloak_manager.get_current_user)): return user

@app.get("/admin", dependencies=[Depends(require_roles(["admin"]))])
async def admin_only(user: KeycloakUser = Depends(keycloak_manager.get_current_user)):
    return {"message": "Admin access", "user": user.username}

class RefreshRequest(BaseModel): refresh_token: str

@app.post("/token/refresh")
async def refresh(req: RefreshRequest):
     try: return await keycloak_manager.refresh_token(req.refresh_token)
     except AuthError as e: return JSONResponse(e.status_code, e.detail)

@app.get("/health/keycloak", response_model=KeycloakDiagnosticResult)
async def keycloak_health(): return await keycloak_manager.run_diagnostics()

@app.on_event("shutdown")
async def shutdown(): await keycloak_manager.close()

# if __name__ == "__main__": uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Configuration (`KeycloakBuilder`)

Use the `KeycloakBuilder` to configure the integration:

*   `.with_server_url(str)`: **Required.** Base URL of your Keycloak server.
*   `.with_realm(str)`: **Required.** Keycloak realm name.
*   `.with_client_id(str)`: **Required.** Client ID of your FastAPI application.
*   `.with_client_secret(Optional[str])`: Required for confidential clients, token introspection, and token refresh.
*   `.with_audience(Union[str, List[str]])`: Sets expected `aud` claim(s). Validation skipped if not set.
*   `.with_issuer(Union[str, List[str]])`: Sets expected `iss` claim(s). Validation skipped if not set. Default uses OIDC discovery.
*   `.with_algorithms(List[str])`: Allowed JWT signing algorithms (default: `["RS256"]`).
*   `.with_jwks_uri(str)`: Explicitly set JWKS URI, overrides OIDC discovery.
*   `.with_introspection_endpoint(str)`: Explicitly set introspection URI, overrides OIDC discovery.
*   `.with_token_endpoint(str)`: Explicitly set token URI, overrides OIDC discovery.
*   `.use_token_introspection(bool)`: If `True`, uses introspection endpoint for validation instead of local JWT checks (default: `False`). Requires client secret.
*   `.enable_token_refresh(bool)`: If `True`, enables the `refresh_token` method on the manager (default: `False`). Requires client secret.
*   `.without_ssl_verification()`: **INSECURE.** Disables SSL certificate checks. Use only for trusted local testing.
*   `.with_cache_settings(ttl: int, size: int)`: Configure JWKS/OIDC cache TTL (seconds, default 3600/7200) and size (default 1).
*   `.with_http_timeouts(connect: int, read: int)`: Configure HTTP client timeouts (seconds, default 5).
*   `.with_openapi_security_scheme(name: str, scopes: Dict[str, str])`: Configure Swagger UI security scheme name and scopes.
*   `.with_metrics_collector(MetricsCollector)`: Provide an instance conforming to the `MetricsCollector` protocol.

## Core Components

*   **`KeycloakManager`**: The main object returned by `builder.build()`. Holds all configured components and provides methods like `authenticate_token`, `refresh_token`, `run_diagnostics`, `get_middleware`, `get_security_scheme`.
*   **`AuthMiddleware`**: FastAPI middleware instance obtained via `manager.get_middleware()`. Handles token extraction and validation for most requests.
*   **`get_current_user`**: FastAPI dependency to retrieve the `KeycloakUser` object from `request.state` (populated by the middleware). Raises 401 if not authenticated.
*   **`require_roles(List[str], require_all=True)`**: FastAPI dependency factory. Returns a dependency that checks if the authenticated user has the required realm or client roles. Raises 403 if check fails.
*   **`require_groups(List[str], require_all=True)`**: FastAPI dependency factory for checking group membership. Raises 403 if check fails.
*   **`KeycloakUser`**: Pydantic model representing the authenticated user's details extracted from the token or introspection result.
*   **`AuthError`**: Base exception class for errors raised by this library. Specific errors like `TokenExpiredError`, `MissingRolesError`, `KeycloakConnectionError` inherit from this.

## Metrics

The library uses a `MetricsCollector` protocol (see `metrics.py`). You can provide your own implementation (e.g., using `prometheus-client`) via `builder.with_metrics_collector()`. Key metrics include:

*   `fc_kc_token_validation_latency_ms` (Histogram, Tags: `method`, `client_id`, `realm`, `error_code`?)
*   `fc_kc_token_validation_total` (Counter, Tags: `method`, `client_id`, `realm`)
*   `fc_kc_token_validation_success_total` (Counter, Tags: `method`, `client_id`, `realm`)
*   `fc_kc_token_validation_failure_total` (Counter, Tags: `method`, `client_id`, `realm`, `error_code`)
*   `fc_kc_token_refresh_latency_ms` (Histogram, Tags: `client_id`, `realm`, `error_code`?)
*   `fc_kc_token_refresh_total` (Counter, Tags: `client_id`, `realm`)
*   `fc_kc_token_refresh_success_total` (Counter, Tags: `client_id`, `realm`)
*   `fc_kc_token_refresh_failure_total` (Counter, Tags: `client_id`, `realm`, `error_code`)
*   `fc_kc_jwks_fetch_latency_ms` (Histogram, Tags: `client_id`, `realm`, `error_code`?)
*   `fc_kc_oidc_fetch_latency_ms` (Histogram, Tags: `client_id`, `realm`, `error_code`?)
*   `fc_kc_jwks_cache_hits_total` (Counter, Tags: `client_id`, `realm`)
*   `fc_kc_jwks_cache_misses_total` (Counter, Tags: `client_id`, `realm`)
*   `fc_kc_errors_total` (Counter, Tags: `error_code`, `client_id`, `realm`)

## Diagnostics

Call `await keycloak_manager.run_diagnostics()` to check connectivity and certificate validity for configured Keycloak endpoints. Returns a `KeycloakDiagnosticResult` Pydantic model.

## Error Handling

The library raises exceptions derived from `AuthError`. These inherit from `fastapi.HTTPException` and contain a `detail` attribute with a structured error message (`{"error": {"code": "...", "message": "...", "details": {...}}}`). You can use FastAPI's exception handlers to customize responses. See `errors.py` for specific error codes.

## Contributing

Please see `CONTRIBUTING.md` for details on how to contribute.

## License

Distributed under the MIT License. See `LICENSE` file for details.

@c0mpiler
