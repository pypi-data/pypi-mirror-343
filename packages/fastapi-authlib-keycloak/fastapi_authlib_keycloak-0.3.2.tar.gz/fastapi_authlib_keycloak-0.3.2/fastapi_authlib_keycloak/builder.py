
import logging
import time
import asyncio
# Import Set for Python 3.8 compatibility
from typing import Optional, Union, List, Dict, Any, TYPE_CHECKING, Set
from pydantic import HttpUrl
from fastapi import Request
# Removed SecurityBaseModel import, keep others
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowImplicit
from fastapi.security.base import SecurityBase

from .config import KeycloakConfig
from .adapter import KeycloakAdapter
from .validator import TokenValidator
from .client import IntrospectionClient
from .models import KeycloakUser, TokenResponse, KeycloakDiagnosticResult, ConnectionStatus, DiagnosticStatus
from .errors import AuthError, TokenInactiveError, TokenRefreshError, KeycloakConfigurationError
from .refresh import RefreshManager
from .metrics import MetricsCollector, NoOpMetricsCollector, METRIC_TOKEN_VALIDATION_TOTAL, METRIC_TOKEN_VALIDATION_SUCCESS, METRIC_TOKEN_VALIDATION_FAILURE, METRIC_ERRORS_TOTAL, TAG_ERROR_CODE, TAG_VALIDATION_METHOD, TAG_CLIENT_ID, TAG_REALM, METRIC_INTROSPECTION_LATENCY, METRIC_JWT_VALIDATION_LATENCY, METRIC_TOKEN_REFRESH_TOTAL, METRIC_TOKEN_REFRESH_SUCCESS, METRIC_TOKEN_REFRESH_FAILURE, METRIC_REFRESH_LATENCY

if TYPE_CHECKING:
    from .middleware import AuthMiddleware

logger = logging.getLogger(__name__)

# Removed the custom OAuth2ImplicitScheme class

class OAuth2KeycloakImplicit(SecurityBase):
    """Helper class for OpenAPI Implicit Flow definition."""
    def __init__(self, authorizationUrl: str, scopes: Optional[Dict[str, str]] = None, scheme_name: Optional[str] = None, auto_error: bool = True):
        scopes = scopes or {}
        flows = OAuthFlowsModel(implicit=OAuthFlowImplicit(authorizationUrl=authorizationUrl, scopes=scopes))
        # Store the dictionary representation compatible with OpenAPI spec
        self.model = {"type": "oauth2", "flows": flows.dict(exclude_unset=True)}
        self.scheme_name = scheme_name or self.__class__.__name__
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Any:
        pass

class KeycloakManager:
    """Holds components, provides methods, handles metrics & diagnostics."""
    def __init__(self, config: KeycloakConfig, adapter: KeycloakAdapter, validator: TokenValidator, metrics_collector: MetricsCollector, refresh_manager: Optional[RefreshManager] = None, introspection_client: Optional[IntrospectionClient] = None):
        self.config = config; self.adapter = adapter; self.validator = validator; self.introspection_client = introspection_client; self.refresh_manager = refresh_manager; self.metrics = metrics_collector
        self.adapter.metrics = metrics_collector; self.validator.metrics = metrics_collector
        if self.introspection_client: self.introspection_client.metrics = metrics_collector
        if self.refresh_manager: self.refresh_manager.metrics = metrics_collector
        self._security_scheme: Optional[SecurityBase] = None; self._openapi_scheme_name: Optional[str] = None; self._openapi_scopes: Optional[Dict[str, str]] = None

    async def authenticate_token(self, token: str) -> KeycloakUser:
        tags = {TAG_CLIENT_ID: self.config.client_id, TAG_REALM: self.config.realm}; self.metrics.increment_counter(METRIC_TOKEN_VALIDATION_TOTAL, tags=tags)
        start = time.perf_counter(); validation_method = "introspection" if self.config.use_introspection else "jwt"; tags[TAG_VALIDATION_METHOD] = validation_method
        try:
            if self.config.use_introspection:
                if not self.introspection_client: raise AuthError(status_code=500, code="config_error", message="Introspection client not configured.")
                logger.debug("Auth via introspection..."); user = await self._authenticate_via_introspection(token); lat = (time.perf_counter() - start) * 1000
                self.metrics.observe_histogram(METRIC_INTROSPECTION_LATENCY, tags=tags, value=lat)
            else:
                logger.debug("Auth via JWT validation..."); user = await self._authenticate_via_jwt(token); lat = (time.perf_counter() - start) * 1000
                self.metrics.observe_histogram(METRIC_JWT_VALIDATION_LATENCY, tags=tags, value=lat)
            self.metrics.increment_counter(METRIC_TOKEN_VALIDATION_SUCCESS, tags=tags); return user
        except AuthError as e:
            lat = (time.perf_counter() - start) * 1000; err_tags = {**tags, TAG_ERROR_CODE: e.code}
            self.metrics.increment_counter(METRIC_TOKEN_VALIDATION_FAILURE, tags=err_tags); self.metrics.increment_counter(METRIC_ERRORS_TOTAL, tags=err_tags)
            metric = METRIC_INTROSPECTION_LATENCY if validation_method == "introspection" else METRIC_JWT_VALIDATION_LATENCY
            self.metrics.observe_histogram(metric, tags=err_tags, value=lat)
            logger.warning(f"Auth failed ({validation_method}): {e.code} - {e.message}"); raise e
        except Exception as e:
             lat = (time.perf_counter() - start) * 1000; err_tags = {**tags, TAG_ERROR_CODE: "unexpected_auth_error"}
             self.metrics.increment_counter(METRIC_TOKEN_VALIDATION_FAILURE, tags=err_tags); self.metrics.increment_counter(METRIC_ERRORS_TOTAL, tags=err_tags)
             metric = METRIC_INTROSPECTION_LATENCY if validation_method == "introspection" else METRIC_JWT_VALIDATION_LATENCY
             self.metrics.observe_histogram(metric, tags=err_tags, value=lat)
             logger.error(f"Unexpected auth error ({validation_method}): {e}", exc_info=True)
             raise AuthError(status_code=500, code="authentication_error", message=f"Unexpected auth error: {e}") from e

    async def _authenticate_via_introspection(self, token: str) -> KeycloakUser:
        intro_res = await self.introspection_client.introspect_token(token)
        if not intro_res.active: logger.warning("Token inactive via introspection."); raise TokenInactiveError()
        user = KeycloakUser.from_introspection(intro_res); logger.info(f"Token introspected for user: {user.username}"); return user

    async def _authenticate_via_jwt(self, token: str) -> KeycloakUser:
         user = await self.validator.validate_token(token); return user

    async def refresh_token(self, refresh_token: str) -> TokenResponse:
        if not self.config.enable_refresh or not self.refresh_manager: raise KeycloakConfigurationError("Refresh not enabled/configured.")
        tags = {TAG_CLIENT_ID: self.config.client_id, TAG_REALM: self.config.realm}; self.metrics.increment_counter(METRIC_TOKEN_REFRESH_TOTAL, tags=tags)
        start = time.perf_counter(); logger.debug("Attempting token refresh...")
        try:
            response = await self.refresh_manager.exchange_refresh_token(refresh_token); lat = (time.perf_counter() - start) * 1000
            self.metrics.observe_histogram(METRIC_REFRESH_LATENCY, tags=tags, value=lat); self.metrics.increment_counter(METRIC_TOKEN_REFRESH_SUCCESS, tags=tags); return response
        except (AuthError, TokenRefreshError) as e:
            lat = (time.perf_counter() - start) * 1000; err_tags = {**tags, TAG_ERROR_CODE: e.code}
            self.metrics.observe_histogram(METRIC_REFRESH_LATENCY, tags=err_tags, value=lat); self.metrics.increment_counter(METRIC_TOKEN_REFRESH_FAILURE, tags=err_tags); self.metrics.increment_counter(METRIC_ERRORS_TOTAL, tags=err_tags)
            logger.warning(f"Refresh failed: {e.code} - {e.message}"); raise e
        except Exception as e:
            lat = (time.perf_counter() - start) * 1000; err_tags = {**tags, TAG_ERROR_CODE: "unexpected_refresh_error"}
            self.metrics.observe_histogram(METRIC_REFRESH_LATENCY, tags=err_tags, value=lat); self.metrics.increment_counter(METRIC_TOKEN_REFRESH_FAILURE, tags=err_tags); self.metrics.increment_counter(METRIC_ERRORS_TOTAL, tags=err_tags)
            logger.error(f"Unexpected refresh error: {e}", exc_info=True); raise TokenRefreshError(code="refresh_unexpected_error", message=f"Unexpected refresh error: {e}") from e

    def get_middleware(self, public_paths: Optional[Set[str]] = None) -> 'AuthMiddleware':
        # This method seems unused based on examples, consider removal or clarification.
        pass

    async def get_authorization_url(self) -> str:
        oidc_config = await self.adapter.get_oidc_config(); auth_endpoint = oidc_config.get("authorization_endpoint")
        if not auth_endpoint: raise KeycloakConfigurationError("Auth endpoint not in OIDC config.")
        return str(auth_endpoint)

    async def get_security_scheme(self) -> SecurityBase:
        """Gets the FastAPI SecurityBase object configured for OpenAPI."""
        scheme_name = self._openapi_scheme_name or "KeycloakAuth"
        scopes = self._openapi_scopes or {}
        if not self._security_scheme:
             try:
                 auth_url = await self.get_authorization_url()
                 self._security_scheme = OAuth2KeycloakImplicit(
                     authorizationUrl=auth_url,
                     scopes=scopes,
                     scheme_name=scheme_name
                 )
                 logger.info(f"Created OpenAPI scheme '{scheme_name}' for {auth_url}")
             except Exception as e:
                 logger.error(f"Failed to create OpenAPI security scheme: {e}", exc_info=True)
                 raise KeycloakConfigurationError(f"Could not get auth URL for OpenAPI: {e}") from e
        return self._security_scheme

    async def run_diagnostics(self) -> KeycloakDiagnosticResult:
        """Performs connectivity and configuration checks."""
        logger.info("Running Keycloak diagnostics...")
        try:
            await self.adapter.get_oidc_config()
        except Exception as e:
             logger.error(f"Diagnostics failed: Could not load OIDC config: {e}", exc_info=True)
             oidc_status = ConnectionStatus(endpoint_url=self.config.get_well_known_endpoint(), status=DiagnosticStatus.ERROR, message=f"Failed to load OIDC config: {e}")
             return KeycloakDiagnosticResult(server_url=str(self.config.server_url), realm=self.config.realm, ssl_verification_enabled=self.config.verify_ssl, oidc_discovery_status=oidc_status, jwks_uri_status=ConnectionStatus(status=DiagnosticStatus.ERROR, message="Skipped due to OIDC failure"))
        oidc_url = self.config.get_well_known_endpoint(); jwks_url = self.config.get_jwks_uri(); intro_url = self.config.get_introspection_endpoint() if self.config.use_introspection else None; token_url = self.config.get_token_endpoint() if self.config.enable_refresh else None
        tasks = [self.adapter.test_connection(oidc_url)];
        if jwks_url: tasks.append(self.adapter.test_connection(jwks_url))
        if intro_url: tasks.append(self.adapter.test_connection(intro_url))
        if token_url: tasks.append(self.adapter.test_connection(token_url))
        results = await asyncio.gather(*tasks)
        oidc_status = results[0]; jwks_status = results[1] if jwks_url else ConnectionStatus(status=DiagnosticStatus.DISABLED, message="JWKS URI not configured/derived.")
        result_index = 2; intro_status = None
        if intro_url: intro_status = results[result_index]; result_index += 1
        elif self.config.use_introspection: intro_status = ConnectionStatus(status=DiagnosticStatus.ERROR, message="Introspection enabled but endpoint not configured/derived.")
        else: intro_status = ConnectionStatus(status=DiagnosticStatus.DISABLED, message="Introspection not enabled.")
        token_status = None
        if token_url: token_status = results[result_index]
        elif self.config.enable_refresh: token_status = ConnectionStatus(status=DiagnosticStatus.ERROR, message="Refresh enabled but endpoint not configured/derived.")
        else: token_status = ConnectionStatus(status=DiagnosticStatus.DISABLED, message="Refresh not enabled.")
        diag_result = KeycloakDiagnosticResult(server_url=str(self.config.server_url), realm=self.config.realm, ssl_verification_enabled=self.config.verify_ssl, oidc_discovery_status=oidc_status, jwks_uri_status=jwks_status, introspection_endpoint_status=intro_status, token_endpoint_status=token_status)
        logger.info(f"Diagnostics completed. Status: OIDC={oidc_status.status}, JWKS={jwks_status.status}")
        return diag_result

    async def close(self): await self.adapter.close()


class KeycloakBuilder:
    def __init__(self):
        self._config_params: dict = {}; self._scopes: Optional[Dict[str, str]] = None; self._scheme_name: str = "KeycloakAuth"; self._metrics_collector: Optional[MetricsCollector] = None
        logger.debug("KeycloakBuilder initialized.")

    def with_server_url(self, url: Union[str, HttpUrl]) -> 'KeycloakBuilder': self._config_params['server_url'] = str(url); return self
    def with_realm(self, realm: str) -> 'KeycloakBuilder': self._config_params['realm'] = realm; return self
    def with_client_id(self, cid: str) -> 'KeycloakBuilder': self._config_params['client_id'] = cid; return self
    def with_client_secret(self, secret: Optional[str]) -> 'KeycloakBuilder': self._config_params['client_secret'] = secret; return self
    def with_client_credentials(self, cid: str, secret: Optional[str]) -> 'KeycloakBuilder': self.with_client_id(cid); self.with_client_secret(secret); return self
    def with_audience(self, aud: Union[str, List[str]]) -> 'KeycloakBuilder': self._config_params['audience'] = aud; return self
    def with_issuer(self, iss: Union[str, List[str]]) -> 'KeycloakBuilder': self._config_params['issuer'] = iss; return self
    def with_algorithms(self, algs: List[str]) -> 'KeycloakBuilder': self._config_params['algorithms'] = algs; return self
    def with_jwks_uri(self, uri: Union[str, HttpUrl]) -> 'KeycloakBuilder': self._config_params['jwks_uri'] = str(uri); return self
    def with_introspection_endpoint(self, uri: Union[str, HttpUrl]) -> 'KeycloakBuilder': self._config_params['introspection_endpoint'] = str(uri); return self
    def with_token_endpoint(self, uri: Union[str, HttpUrl]) -> 'KeycloakBuilder': self._config_params['token_endpoint'] = str(uri); return self
    def with_cache_settings(self, ttl: int = 3600, size: int = 1) -> 'KeycloakBuilder': self._config_params['cache_ttl'] = ttl; self._config_params['cache_maxsize'] = size; return self
    def with_http_timeouts(self, conn: int = 5, read: int = 5) -> 'KeycloakBuilder': self._config_params['connect_timeout'] = conn; self._config_params['read_timeout'] = read; return self
    def without_ssl_verification(self) -> 'KeycloakBuilder': logger.warning("Disabling SSL verification."); self._config_params['verify_ssl'] = False; return self
    def use_token_introspection(self, use: bool = True) -> 'KeycloakBuilder': self._config_params['use_introspection'] = use; return self
    def enable_token_refresh(self, enable: bool = True) -> 'KeycloakBuilder': self._config_params['enable_refresh'] = enable; return self
    def with_openapi_security_scheme(self, name: str = "KeycloakAuth", scopes: Optional[Dict[str, str]] = None) -> 'KeycloakBuilder': self._scheme_name = name; self._scopes = scopes; return self
    def with_metrics_collector(self, coll: MetricsCollector) -> 'KeycloakBuilder': self._metrics_collector = coll; return self

    def build(self) -> KeycloakManager:
        logger.info("Building Keycloak components...")
        try: config = KeycloakConfig(**self._config_params)
        except Exception as e: logger.error(f"Config error: {e}", exc_info=True); raise ValueError(f"Invalid config: {e}") from e
        if config.use_introspection and not config.client_secret: raise ValueError("Client secret needed for introspection.")
        if config.enable_refresh and not config.client_secret: raise ValueError("Client secret needed for refresh.")
        metrics = self._metrics_collector or NoOpMetricsCollector(); logger.info(f"Using metrics: {type(metrics).__name__}")
        adapter = KeycloakAdapter(config=config, metrics=metrics)
        validator = TokenValidator(config=config, adapter=adapter, metrics=metrics)
        intro_client = IntrospectionClient(config=config, adapter=adapter, metrics=metrics) if config.use_introspection else None
        ref_manager = RefreshManager(config=config, adapter=adapter, metrics=metrics) if config.enable_refresh else None
        manager = KeycloakManager(config=config, adapter=adapter, validator=validator, introspection_client=intro_client, refresh_manager=ref_manager, metrics_collector=metrics)
        logger.info("KeycloakManager built.")
        manager._openapi_scheme_name = self._scheme_name
        manager._openapi_scopes = self._scopes
        return manager
