
import httpx
import logging
import time
import ssl
import certifi
import socket
import datetime
from urllib.parse import urlparse
from cachetools import TTLCache
from typing import Dict, Any, Optional

from .config import KeycloakConfig
from .errors import KeycloakConfigurationError, KeycloakConnectionError, CertError, CertExpiredError, CertUntrustedError, HostnameMismatchError, AuthError
from .metrics import MetricsCollector, NoOpMetricsCollector, METRIC_JWKS_FETCH_LATENCY, METRIC_OIDC_FETCH_LATENCY, METRIC_ERRORS_TOTAL, TAG_ERROR_CODE, TAG_REALM, TAG_CLIENT_ID, METRIC_JWKS_CACHE_HITS, METRIC_JWKS_CACHE_MISSES
from .models import ConnectionStatus, DiagnosticStatus # Added diagnostics models

logger = logging.getLogger(__name__)

class KeycloakAdapter:
    """Handles communication with Keycloak, caching, metrics, and diagnostics."""

    def __init__(self, config: KeycloakConfig, metrics: Optional[MetricsCollector] = None):
        self.config = config
        self.metrics = metrics or NoOpMetricsCollector()
        self._jwks_cache = TTLCache(maxsize=1, ttl=self.config.cache_ttl) 
        self._oidc_config_cache = TTLCache(maxsize=1, ttl=self.config.cache_ttl * 2)
        self._metric_tags = {TAG_REALM: config.realm, TAG_CLIENT_ID: config.client_id}
        self._ssl_context = self._create_ssl_context() # Store context
        self._http_client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.config.connect_timeout, read=self.config.read_timeout),
            verify=self._ssl_context if self.config.verify_ssl else False, # Use context or False
            http2=True
        )
        logger.info(f"Adapter initialized for realm '{config.realm}' at {config.server_url}")

    def _create_ssl_context(self) -> Optional[ssl.SSLContext]:
        # If verification is disabled, return None
        if not self.config.verify_ssl:
            logger.warning("SSL verification is DISABLED. Connection is insecure.")
            return None 
        # Otherwise, create and return a default context using certifi
        try:
             logger.info(f"Creating SSL context with CA bundle from: {certifi.where()}")
             return ssl.create_default_context(cafile=certifi.where())
        except Exception as e:
             logger.error(f"Failed to create SSL context: {e}", exc_info=True)
             # Propagate error - adapter cannot function securely without a context
             raise KeycloakConfigurationError(f"Failed to initialize SSL context: {e}") from e

    async def close(self): await self._http_client.aclose(); logger.info("Adapter HTTP client closed.")

    async def get_oidc_config(self) -> Dict[str, Any]:
        # ... (implementation remains the same, uses _handle_fetch_error)
        oidc_config = self._oidc_config_cache.get('oidc_config');
        if oidc_config: return oidc_config
        well_known_url = self.config.get_well_known_endpoint()
        logger.debug(f"Fetching OIDC config from: {well_known_url}")
        start_time = time.perf_counter()
        try:
            response = await self._http_client.get(well_known_url)
            latency = (time.perf_counter() - start_time) * 1000
            self.metrics.observe_histogram(METRIC_OIDC_FETCH_LATENCY, tags=self._metric_tags, value=latency)
            response.raise_for_status()
            oidc_config = response.json()
            logger.info(f"Fetched OIDC config from {well_known_url}")
            if not self.config.jwks_uri and "jwks_uri" in oidc_config: self.config._derived_jwks_uri = oidc_config["jwks_uri"]
            if not self.config.introspection_endpoint and "introspection_endpoint" in oidc_config: self.config._derived_introspection_endpoint = oidc_config["introspection_endpoint"]
            if not self.config.token_endpoint and "token_endpoint" in oidc_config: self.config._derived_token_endpoint = oidc_config["token_endpoint"]
            self._oidc_config_cache['oidc_config'] = oidc_config
            return oidc_config
        except Exception as e:
            latency = (time.perf_counter() - start_time) * 1000
            error_code = self._get_error_code(e)
            error_tags = {**self._metric_tags, TAG_ERROR_CODE: error_code}
            self.metrics.observe_histogram(METRIC_OIDC_FETCH_LATENCY, tags=error_tags, value=latency)
            self.metrics.increment_counter(METRIC_ERRORS_TOTAL, tags=error_tags)
            self._handle_fetch_error(e, well_known_url, "OIDC config")

    async def get_jwks(self) -> Dict[str, Any]:
        # ... (implementation remains the same, uses _handle_fetch_error)
        jwks = self._jwks_cache.get('jwks'); 
        if jwks: self.metrics.increment_counter(METRIC_JWKS_CACHE_HITS, tags=self._metric_tags); return jwks
        self.metrics.increment_counter(METRIC_JWKS_CACHE_MISSES, tags=self._metric_tags)
        jwks_uri = self.config.get_jwks_uri()
        if not jwks_uri: await self.get_oidc_config(); jwks_uri = self.config.get_jwks_uri()
        if not jwks_uri: raise KeycloakConfigurationError("JWKS URI unavailable.")
        logger.debug(f"Fetching JWKS from: {jwks_uri}")
        start_time = time.perf_counter()
        try:
            response = await self._http_client.get(jwks_uri)
            latency = (time.perf_counter() - start_time) * 1000
            self.metrics.observe_histogram(METRIC_JWKS_FETCH_LATENCY, tags=self._metric_tags, value=latency)
            response.raise_for_status()
            jwks = response.json()
            if "keys" not in jwks or not isinstance(jwks["keys"], list): raise KeycloakConfigurationError(f"Invalid JWKS format from {jwks_uri}")
            logger.info(f"Fetched {len(jwks['keys'])} keys from JWKS: {jwks_uri}")
            self._jwks_cache['jwks'] = jwks
            return jwks
        except Exception as e:
            latency = (time.perf_counter() - start_time) * 1000
            error_code = self._get_error_code(e)
            error_tags = {**self._metric_tags, TAG_ERROR_CODE: error_code}
            self.metrics.observe_histogram(METRIC_JWKS_FETCH_LATENCY, tags=error_tags, value=latency)
            self.metrics.increment_counter(METRIC_ERRORS_TOTAL, tags=error_tags)
            self._handle_fetch_error(e, jwks_uri, "JWKS")

    async def get_jwk_for_kid(self, kid: str) -> Optional[Dict[str, Any]]:
        # ... (implementation remains the same)
        jwks = self._jwks_cache.get('jwks')
        if jwks:
             key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
             if key: self.metrics.increment_counter(METRIC_JWKS_CACHE_HITS, tags=self._metric_tags); return key
        logger.warning(f"Kid '{kid}' not in cache/stale. Fetching JWKS.")
        self._jwks_cache.clear()
        try:
            refreshed_jwks = await self.get_jwks()
            key = next((k for k in refreshed_jwks.get("keys", []) if k.get("kid") == kid), None)
            if key: logger.info(f"Found JWK for kid '{kid}' after refresh."); return key
            else: logger.error(f"Kid '{kid}' not found after refresh."); self.metrics.increment_counter(METRIC_ERRORS_TOTAL, tags={**self._metric_tags, TAG_ERROR_CODE: "unknown_kid_after_refresh"}); return None
        except Exception as e: logger.error(f"Error refreshing JWKS for kid '{kid}': {e}", exc_info=True); raise e

    async def test_connection(self, url: str) -> ConnectionStatus:
        """Tests HTTP(S) connection and SSL certificate validity for a given URL."""
        status = ConnectionStatus(endpoint_url=url)
        if not self.config.verify_ssl:
            status.status = DiagnosticStatus.DISABLED
            status.message = "SSL verification is disabled."
            # Can still attempt connection

        logger.debug(f"Testing connection to: {url}")
        start_time = time.perf_counter()
        try:
            # Make a HEAD request as it's lightweight
            response = await self._http_client.head(url, timeout=5.0) # Use shorter timeout
            latency = (time.perf_counter() - start_time) * 1000
            status.latency_ms = round(latency, 2)
            
            # Check basic connectivity (any 2xx, 3xx, or even 401/403 is usually OK for connectivity)
            if 400 <= response.status_code < 500:
                 logger.warning(f"Connection test to {url} received HTTP {response.status_code}. Treating as OK for connectivity test.")
                 status.message = f"Connected, but received HTTP {response.status_code}."
            elif response.status_code >= 500:
                 raise httpx.HTTPStatusError(f"Server error: {response.status_code}", request=response.request, response=response)
            else:
                 status.message = f"Connected successfully (HTTP {response.status_code})."
                 
            # If SSL verification is enabled, check certificate details via underlying socket
            if self.config.verify_ssl and url.lower().startswith("https://"):
                 status.cert_valid, status.cert_expiry_days_remaining, status.cert_error_details = self._check_certificate_details(url)
                 if status.cert_valid is False:
                     status.status = DiagnosticStatus.ERROR # Override status if cert is invalid
                     status.message = f"Certificate validation failed: {status.cert_error_details}"
                 elif status.cert_expiry_days_remaining is not None and status.cert_expiry_days_remaining < 30:
                     logger.warning(f"Certificate for {url} expires in {status.cert_expiry_days_remaining} days.")
                     # Don't set status to ERROR, but message reflects warning
                     status.message += f" Warning: Certificate expires in {status.cert_expiry_days_remaining} days."

        except Exception as e:
            latency = (time.perf_counter() - start_time) * 1000
            status.latency_ms = round(latency, 2)
            status.status = DiagnosticStatus.ERROR
            status.message = f"Connection failed: {type(e).__name__} - {e}"
            logger.warning(f"Connection test failed for {url}: {e}")
            
            # Try to extract certificate error details if it was an SSL error
            if isinstance(e, ssl.SSLCertVerificationError):
                 status.cert_valid = False
                 status.cert_error_details = str(e)
                 if "expired" in str(e): status.message = "Connection failed: Certificate expired."
                 elif "hostname mismatch" in str(e): status.message = "Connection failed: Certificate hostname mismatch."
                 elif "unable to get local issuer" in str(e) or "verify failed" in str(e): status.message = "Connection failed: Certificate not trusted."
                 else: status.message = f"Connection failed: SSL verification error - {e}"
            elif isinstance(e, ssl.SSLError):
                 status.cert_valid = False # General SSL error
                 status.cert_error_details = str(e)
                 status.message = f"Connection failed: SSL error - {e}"
            elif isinstance(e, httpx.TimeoutException): status.message = "Connection failed: Timeout."
            elif isinstance(e, httpx.ConnectError): status.message = f"Connection failed: Network error - {e}"
            # Keep the generic message for other exceptions
        return status

    def _check_certificate_details(self, url: str) -> (Optional[bool], Optional[int], Optional[str]):
        """Uses standard library ssl to get cert details. Returns (isValid, daysRemaining, errorMsg)."""
        if not self._ssl_context: return None, None, "SSL verification disabled in config"
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc.split(':')[0] # Get hostname without port
        port = parsed_url.port or 443
        
        try:
            # Connect socket and perform TLS handshake
            with socket.create_connection((hostname, port), timeout=self.config.connect_timeout) as sock:
                 with self._ssl_context.wrap_socket(sock, server_hostname=hostname) as ssock:
                      cert = ssock.getpeercert()
                      
            # Check expiry date
            expiry_date_str = cert.get('notAfter')
            if not expiry_date_str: return True, None, "Could not determine expiry date from certificate."
            
            # Parse expiry date (format: 'Month Day HH:MM:SS YYYY GMT')
            expiry_date = datetime.datetime.strptime(expiry_date_str, '%b %d %H:%M:%S %Y %Z')
            # Ensure timezone awareness for comparison
            expiry_date = expiry_date.replace(tzinfo=datetime.timezone.utc)
            now = datetime.datetime.now(datetime.timezone.utc)
            
            days_remaining = (expiry_date - now).days
            
            if days_remaining < 0:
                 return False, days_remaining, f"Certificate expired on {expiry_date_str}"
            
            # Hostname check is implicitly done by context.wrap_socket if check_hostname=True
            # Trust check is implicitly done by context loading CAs
            return True, days_remaining, None
            
        except ssl.SSLCertVerificationError as e:
            logger.debug(f"Cert verification failed during diagnostic check for {url}: {e}")
            return False, None, str(e)
        except ssl.SSLError as e: # Includes hostname mismatch
            logger.debug(f"SSL error during diagnostic check for {url}: {e}")
            return False, None, str(e)
        except socket.timeout:
            logger.debug(f"Socket timeout during diagnostic check for {url}")
            return None, None, "Socket timeout during connection"
        except Exception as e: # Other errors (DNS lookup, connection refused etc.)
            logger.debug(f"Error during diagnostic check for {url}: {e}")
            return None, None, f"{type(e).__name__}: {e}"

    def _get_error_code(self, e: Exception) -> str: # Keep this helper
        if isinstance(e, KeycloakConnectionError): return e.code
        if isinstance(e, AuthError): return e.code
        if isinstance(e, httpx.TimeoutException): return "timeout"
        if isinstance(e, httpx.HTTPStatusError): return f"http_{e.response.status_code}"
        if isinstance(e, ssl.SSLError): return "ssl_error"
        if isinstance(e, httpx.RequestError): return "connection_error"
        return "unexpected_adapter_error"

    def _handle_fetch_error(self, e: Exception, url: str, context: str): # Keep this helper
        error_code = self._get_error_code(e); logger.error(f"Error fetching {context} from {url}: {error_code} - {e}", exc_info=True)
        if isinstance(e, httpx.TimeoutException): raise KeycloakConnectionError(code=f"{context.lower()}_timeout", message=f"Timeout fetching {context} from {url}") from e
        if isinstance(e, httpx.HTTPStatusError): raise KeycloakConfigurationError(f"HTTP error fetching {context} ({e.response.status_code}): {url}", details={"status_code": e.response.status_code, "response": e.response.text}) from e
        if isinstance(e, ssl.SSLCertVerificationError):
            if "expired" in str(e): raise CertExpiredError(f"Cert for {url} expired.") from e
            if "unable to get local issuer" in str(e) or "verify failed" in str(e): raise CertUntrustedError(f"Could not verify cert for {url}.") from e
            raise CertError(code="cert_verify_failed", message=f"SSL verify failed for {url}: {e}") from e
        if isinstance(e, ssl.SSLError):
             if "hostname mismatch" in str(e): raise HostnameMismatchError(f"Hostname mismatch for {url}.") from e
             raise KeycloakConnectionError(code="ssl_error", message=f"SSL error for {url}: {e}") from e
        if isinstance(e, httpx.RequestError): raise KeycloakConnectionError(message=f"Network error fetching {context} from {url}") from e
        if isinstance(e, KeycloakConfigurationError): raise e
        raise KeycloakConfigurationError(f"Unexpected error fetching {context} from {url}: {e}") from e

