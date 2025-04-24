
import httpx
import logging
import ssl
import time
from typing import Optional
from pydantic import BaseModel # Import BaseModel here

from .config import KeycloakConfig
from .adapter import KeycloakAdapter
from .errors import (
    KeycloakConfigurationError, KeycloakConnectionError, AuthError, 
    CertError, CertExpiredError, CertUntrustedError, HostnameMismatchError,
    TokenRefreshError
)
from .models import TokenResponse
from .metrics import MetricsCollector, NoOpMetricsCollector, METRIC_REFRESH_LATENCY, METRIC_ERRORS_TOTAL, TAG_ERROR_CODE, TAG_REALM, TAG_CLIENT_ID # Added

logger = logging.getLogger(__name__)

class RefreshManager:
    """Handles token refresh calls and related metrics."""

    def __init__(self, config: KeycloakConfig, adapter: KeycloakAdapter, metrics: Optional[MetricsCollector] = None):
        self.config = config
        self.adapter = adapter
        self.metrics = metrics or NoOpMetricsCollector() # Added
        self._metric_tags = {TAG_REALM: config.realm, TAG_CLIENT_ID: config.client_id} # Added
        if not config.enable_refresh: logger.warning("RefreshManager: enable_refresh=False.")
        if not self.config.client_id or not self.config.client_secret: logger.warning("RefreshManager: client creds missing.")
        logger.info("Refresh Manager initialized.")
        
    async def exchange_refresh_token(self, refresh_token: str) -> TokenResponse:
        if not self.config.enable_refresh: raise KeycloakConfigurationError("Token refresh disabled.")
            
        token_endpoint = self.config.get_token_endpoint()
        if not token_endpoint:
            await self.adapter.get_oidc_config() # Let adapter handle discovery
            token_endpoint = self.config.get_token_endpoint()
            if not token_endpoint: raise KeycloakConfigurationError("Token endpoint unavailable.")

        if not self.config.client_id or not self.config.client_secret: raise KeycloakConfigurationError("Client ID/Secret needed for refresh.")

        data = {
            "grant_type": "refresh_token", "refresh_token": refresh_token,
            "client_id": self.config.client_id, "client_secret": self.config.client_secret,
        }
        
        logger.debug(f"Exchanging refresh token via: {token_endpoint}")
        start_time = time.perf_counter() # Added timing
        try:
            response = await self.adapter._http_client.post(token_endpoint, data=data)
            latency = (time.perf_counter() - start_time) * 1000 # Added latency calculation
            # Don't record histogram here, let KeycloakManager record overall refresh latency
            
            response.raise_for_status() 

            # Success - manager records overall latency and success counter
            # self.metrics.observe_histogram(METRIC_REFRESH_LATENCY, tags=self._metric_tags, value=latency)

            result_json = response.json()
            token_response = TokenResponse(**result_json)
            logger.info(f"Successfully refreshed token for client '{self.config.client_id}'.")
            return token_response

        except Exception as e:
             # Record latency on failure
            latency = (time.perf_counter() - start_time) * 1000
            error_code = self._get_error_code(e)
            error_tags = {**self._metric_tags, TAG_ERROR_CODE: error_code}
            # Let manager record overall latency and error counters
            # self.metrics.observe_histogram(METRIC_REFRESH_LATENCY, tags=error_tags, value=latency)
            # self.metrics.increment_counter(METRIC_ERRORS_TOTAL, tags=error_tags)
            self._handle_refresh_error(e, token_endpoint)
            
    def _get_error_code(self, e: Exception) -> str:
        "Helper to get a consistent error code tag." 
        if isinstance(e, KeycloakConnectionError): return e.code
        if isinstance(e, AuthError): return e.code
        if isinstance(e, TokenRefreshError): return e.code
        if isinstance(e, httpx.TimeoutException): return "timeout"
        if isinstance(e, httpx.HTTPStatusError):
             try:
                 payload = e.response.json()
                 return payload.get("error", f"http_{e.response.status_code}")
             except Exception:
                 return f"http_{e.response.status_code}"
        if isinstance(e, ssl.SSLError): return "ssl_error"
        if isinstance(e, httpx.RequestError): return "connection_error"
        return "unexpected_refresh_error"

    def _handle_refresh_error(self, e: Exception, url: str):
        "Helper to log and raise appropriate exceptions for refresh errors." 
        error_code = self._get_error_code(e)
        logger.warning(f"Error refreshing token at {url}: {error_code} - {e}", exc_info=True)

        if isinstance(e, httpx.TimeoutException): raise KeycloakConnectionError(code="refresh_timeout", message=f"Timeout refreshing token at {url}") from e
        if isinstance(e, httpx.HTTPStatusError):
            details = {"status_code": e.response.status_code, "response": e.response.text}
            try: payload = e.response.json(); err = payload.get("error", "http_error"); desc = payload.get("error_description","")
            except: err = f"http_{e.response.status_code}"; desc = e.response.text
            
            status = e.response.status_code
            # Map specific OAuth2 errors for refresh
            if err == "invalid_grant": raise TokenRefreshError(code="invalid_grant", message=f"Invalid refresh grant: {desc}", status_code=status, details=details) from e
            if err == "invalid_client": raise AuthError(status_code=status, code="invalid_client", message=f"Invalid client creds: {desc}", details=details) from e
            if err == "unauthorized_client": raise AuthError(status_code=status, code="unauthorized_client", message=f"Client not authorized for refresh: {desc}", details=details) from e
            # General HTTP error during refresh
            raise TokenRefreshError(code=f"refresh_{err}", message=f"HTTP error during refresh ({err}): {desc}", status_code=status, details=details) from e
        # Handle SSL errors
        if isinstance(e, ssl.SSLCertVerificationError):
            if "expired" in str(e): raise CertExpiredError(f"Cert for {url} expired.") from e
            if "unable to get local issuer" in str(e) or "verify failed" in str(e): raise CertUntrustedError(f"Could not verify cert for {url}.") from e
            raise CertError(code="cert_verify_failed", message=f"SSL verify failed for {url}: {e}") from e
        if isinstance(e, ssl.SSLError):
             if "hostname mismatch" in str(e): raise HostnameMismatchError(f"Hostname mismatch for {url}.") from e
             raise KeycloakConnectionError(code="ssl_error", message=f"SSL error for {url}: {e}") from e
        if isinstance(e, httpx.RequestError): raise KeycloakConnectionError(message=f"Network error refreshing token at {url}") from e
        # Fallback
        response_text = getattr(getattr(e, 'response', None), 'text', '<no response text>')
        raise TokenRefreshError(code="refresh_unexpected_error", message=f"Unexpected refresh error: {e}", details={"response": response_text}) from e
