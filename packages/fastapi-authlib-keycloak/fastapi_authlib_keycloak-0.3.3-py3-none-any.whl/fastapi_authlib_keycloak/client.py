
import httpx
import logging
import ssl
import time
from typing import Optional

from .config import KeycloakConfig
from .adapter import KeycloakAdapter 
from .models import IntrospectionResult
from .errors import (
    KeycloakConfigurationError, KeycloakConnectionError, AuthError, 
    CertError, CertExpiredError, CertUntrustedError, HostnameMismatchError, 
    TokenInactiveError # Import needed for raising
)
from .metrics import MetricsCollector, NoOpMetricsCollector, METRIC_INTROSPECTION_LATENCY, METRIC_ERRORS_TOTAL, TAG_ERROR_CODE, TAG_REALM, TAG_CLIENT_ID # Added

logger = logging.getLogger(__name__)

class IntrospectionClient:
    """Handles introspection calls and related metrics."""

    def __init__(self, config: KeycloakConfig, adapter: KeycloakAdapter, metrics: Optional[MetricsCollector] = None):
        self.config = config
        self.adapter = adapter
        self.metrics = metrics or NoOpMetricsCollector() # Added
        self._metric_tags = {TAG_REALM: config.realm, TAG_CLIENT_ID: config.client_id} # Added
        if not self.config.client_id or not self.config.client_secret: logger.warning("IntrospectionClient: client creds missing.")
        logger.info("Introspection Client initialized.")

    async def introspect_token(self, token: str, token_type_hint: str = "access_token") -> IntrospectionResult:
        introspection_endpoint = self.config.get_introspection_endpoint()
        if not introspection_endpoint:
            await self.adapter.get_oidc_config() # Let adapter handle discovery errors
            introspection_endpoint = self.config.get_introspection_endpoint()
            if not introspection_endpoint: raise KeycloakConfigurationError("Introspection endpoint unavailable.")

        if not self.config.client_id or not self.config.client_secret: raise KeycloakConfigurationError("Client ID/Secret required for introspection.")

        data = {"token": token, "token_type_hint": token_type_hint}
        auth = (self.config.client_id, self.config.client_secret)

        logger.debug(f"Introspecting token via: {introspection_endpoint}")
        start_time = time.perf_counter() # Added timing
        try:
            response = await self.adapter._http_client.post(introspection_endpoint, data=data, auth=auth)
            latency = (time.perf_counter() - start_time) * 1000 # Added latency calculation
            # Don't record latency histogram here; let KeycloakManager record overall auth latency
            
            # Raise HTTP errors (4xx, 5xx)
            response.raise_for_status()
            
            # We got a 2xx - record latency for successful HTTP call
            # Let manager record overall latency including JSON parsing etc.
            # self.metrics.observe_histogram(METRIC_INTROSPECTION_LATENCY, tags=self._metric_tags, value=latency)
            
            result_json = response.json()
            introspection_result = IntrospectionResult(**result_json)
            logger.debug(f"Introspection HTTP call successful (active={introspection_result.active})")
            
            # IntrospectionResult is returned, KeycloakManager handles active check & user creation
            return introspection_result
            
        except Exception as e:
            # Record latency on failure
            latency = (time.perf_counter() - start_time) * 1000
            error_code = self._get_error_code(e)
            error_tags = {**self._metric_tags, TAG_ERROR_CODE: error_code}
            # Let manager record overall latency on error
            # self.metrics.observe_histogram(METRIC_INTROSPECTION_LATENCY, tags=error_tags, value=latency)
            # Manager will increment METRIC_ERRORS_TOTAL
            self._handle_introspection_error(e, introspection_endpoint) # Log and raise specific error

    def _get_error_code(self, e: Exception) -> str:
        "Helper to get a consistent error code tag." 
        if isinstance(e, KeycloakConnectionError): return e.code
        if isinstance(e, AuthError): return e.code # Includes CertError, TokenInactiveError
        if isinstance(e, httpx.TimeoutException): return "timeout"
        if isinstance(e, httpx.HTTPStatusError):
             try: # Check for OAuth2 error in body
                 payload = e.response.json()
                 # Use Keycloak/OAuth2 error code if available, else use HTTP status
                 return payload.get("error", f"http_{e.response.status_code}")
             except Exception:
                 return f"http_{e.response.status_code}"
        if isinstance(e, ssl.SSLError): return "ssl_error"
        if isinstance(e, httpx.RequestError): return "connection_error"
        return "unexpected_introspection_error"

    def _handle_introspection_error(self, e: Exception, url: str):
        "Helper to log and raise appropriate exceptions for introspection errors." 
        error_code = self._get_error_code(e)
        logger.warning(f"Error introspecting token at {url}: {error_code} - {e}", exc_info=True)

        if isinstance(e, httpx.TimeoutException): raise KeycloakConnectionError(code="introspection_timeout", message=f"Timeout introspecting at {url}") from e
        if isinstance(e, httpx.HTTPStatusError):
            details = {"status_code": e.response.status_code, "response": e.response.text}
            if e.response.status_code == 401: raise AuthError(status_code=401, code="invalid_client_credentials", message="Invalid client credentials for introspection.", details=details) from e
            if e.response.status_code == 400:
                 # Keycloak might return specific errors like invalid_token in body
                 try: payload = e.response.json(); err = payload.get("error"); desc = payload.get("error_description","")
                 except: err = "bad_request"; desc = e.response.text
                 # Don't raise TokenInactiveError here, let KeycloakManager check active status
                 # if err == "invalid_token": raise InvalidTokenError(...) 
                 raise AuthError(status_code=400, code=f"introspection_{err}", message=f"Introspection error ({err}): {desc}", details=details) from e
            # Other HTTP errors
            raise AuthError(status_code=e.response.status_code, code=f"introspection_http_{e.response.status_code}", message=f"HTTP {e.response.status_code} during introspection.", details=details) from e
        # Handle SSL errors from adapter._handle_fetch_error pattern
        if isinstance(e, ssl.SSLCertVerificationError):
            if "expired" in str(e): raise CertExpiredError(f"Cert for {url} expired.") from e
            if "unable to get local issuer" in str(e) or "verify failed" in str(e): raise CertUntrustedError(f"Could not verify cert for {url}.") from e
            raise CertError(code="cert_verify_failed", message=f"SSL verify failed for {url}: {e}") from e
        if isinstance(e, ssl.SSLError):
             if "hostname mismatch" in str(e): raise HostnameMismatchError(f"Hostname mismatch for {url}.") from e
             raise KeycloakConnectionError(code="ssl_error", message=f"SSL error for {url}: {e}") from e
        if isinstance(e, httpx.RequestError): raise KeycloakConnectionError(message=f"Network error during introspection at {url}") from e
        # Fallback
        response_text = getattr(getattr(e, 'response', None), 'text', '<no response text>')
        raise AuthError(status_code=500, code="introspection_unexpected_error", message=f"Unexpected introspection error: {e}", details={"response": response_text}) from e

