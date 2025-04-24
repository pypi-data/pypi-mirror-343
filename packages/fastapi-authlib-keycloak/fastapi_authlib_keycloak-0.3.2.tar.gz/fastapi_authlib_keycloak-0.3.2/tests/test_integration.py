
import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from pydantic import BaseModel
# Removed Middleware import

from fastapi_authlib_keycloak import (
    KeycloakBuilder,
    KeycloakManager,
    KeycloakUser,
    get_current_user,
    require_roles,
    AuthError,
    AuthMiddleware, # Need the class for add_middleware
    KeycloakConfig 
)

from .conftest import create_test_token, MOCK_SERVER_URL, MOCK_REALM, MOCK_CLIENT_ID, MOCK_CLIENT_SECRET, MOCK_ISSUER, test_rsa_key_pair

# --- Test FastAPI App Setup --- 

@pytest.fixture(scope="module")
def keycloak_manager_instance(test_rsa_key_pair) -> KeycloakManager:
    builder = KeycloakBuilder() \
        .with_server_url(MOCK_SERVER_URL) \
        .with_realm(MOCK_REALM) \
        .with_client_id(MOCK_CLIENT_ID) \
        .with_client_secret(MOCK_CLIENT_SECRET) \
        .without_ssl_verification() \
        .with_issuer(MOCK_ISSUER) \
        .with_audience(MOCK_CLIENT_ID)
    manager = builder.build()
    return manager

@pytest.fixture(scope="module")
def test_app(keycloak_manager_instance: KeycloakManager) -> FastAPI:
    app = FastAPI(title="Integration Test App")
    
    # Corrected: Use app.add_middleware with the CLASS and kwargs
    # Added "/public" to public_paths
    app.add_middleware(
        AuthMiddleware, # Pass the class itself
        manager=keycloak_manager_instance, # Pass args as kwargs
        public_paths={"/docs", "/openapi.json", "/public"} # Added /public
    )

    @app.exception_handler(AuthError)
    async def auth_error_handler(request, exc):
        from fastapi.responses import JSONResponse
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    @app.get("/public")
    def public_route():
        return {"message": "ok"}

    @app.get("/private", response_model=KeycloakUser)
    def private_route(user: KeycloakUser = Depends(get_current_user)):
        return user

    @app.get("/admin", dependencies=[Depends(require_roles(["admin"]))])
    def admin_route(user: KeycloakUser = Depends(get_current_user)):
        return {"message": "admin access granted", "user": user.username}
        
    # Use lifespan context manager
    from contextlib import asynccontextmanager
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Test App Lifespan: Startup")
        yield
        print("Test App Lifespan: Shutdown")
        await keycloak_manager_instance.close()
        
    app.router.lifespan_context = lifespan

    return app

@pytest.fixture(scope="module")
def client(test_app: FastAPI) -> TestClient:
    with TestClient(test_app) as test_client:
        yield test_client

# --- Integration Tests --- 

# ... (rest of the tests remain the same) ...

def test_public_route_no_auth(client: TestClient):
    response = client.get("/public") # This should now be correctly identified as public
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

def test_private_route_no_auth(client: TestClient):
    response = client.get("/private")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "missing_header"

def test_private_route_invalid_bearer(client: TestClient):
    response = client.get("/private", headers={"Authorization": "Invalid Scheme"})
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_header_format"

def test_private_route_invalid_token(client: TestClient):
    response = client.get("/private", headers={"Authorization": "Bearer invalid-token"})
    # Changed expected status code back to 400 based on InvalidTokenError
    assert response.status_code == 400 
    assert response.json()["error"]["code"] == "malformed_token"

def test_private_route_valid_token(
    client: TestClient, 
    test_rsa_key_pair: dict 
):
    token = create_test_token(test_rsa_key_pair, payload_override={
        "preferred_username": "integ-user",
        "realm_access": {"roles": ["user", "tester"]}
    })
    response = client.get("/private", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == "integ-user"
    assert "user" in user_data["roles"]
    assert "tester" in user_data["roles"]

def test_admin_route_missing_role(
    client: TestClient, 
    test_rsa_key_pair: dict
):
    token = create_test_token(test_rsa_key_pair, payload_override={
        "realm_access": {"roles": ["user"]}
    })
    response = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "missing_roles"
    assert "admin" in response.json()["error"]["details"]["required_roles"]

def test_admin_route_sufficient_role(
    client: TestClient, 
    test_rsa_key_pair: dict
):
    token = create_test_token(test_rsa_key_pair, payload_override={
        "realm_access": {"roles": ["user", "admin"]}
    })
    response = client.get("/admin", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "admin access granted"
    assert response.json()["user"] == "testuser"

