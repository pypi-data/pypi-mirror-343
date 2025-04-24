
from typing import Protocol, Optional, Dict, List

class MetricsCollector(Protocol):
    """Defines the interface for collecting metrics within the library."""

    def increment_counter(
        self, 
        name: str, 
        tags: Optional[Dict[str, str]] = None, 
        value: int = 1
    ) -> None:
        """Increments a counter metric."""
        ...

    def observe_histogram(
        self, 
        name: str, 
        tags: Optional[Dict[str, str]] = None, 
        value: float = 1.0
    ) -> None:
        """Observes a value for a histogram/summary metric (e.g., latency)."""
        ...

    def set_gauge(
        self, 
        name: str, 
        tags: Optional[Dict[str, str]] = None, 
        value: float = 1.0
    ) -> None:
        """Sets a gauge metric to a specific value."""
        ...

class NoOpMetricsCollector:
    """A default implementation that does nothing. Used if no collector is provided."""

    def increment_counter(self, name: str, tags: Optional[Dict[str, str]] = None, value: int = 1) -> None:
        pass

    def observe_histogram(self, name: str, tags: Optional[Dict[str, str]] = None, value: float = 1.0) -> None:
        pass

    def set_gauge(self, name: str, tags: Optional[Dict[str, str]] = None, value: float = 1.0) -> None:
        pass

# --- Standard Metric Names --- (Defined here for consistency)

METRIC_JWT_VALIDATION_LATENCY = "fc_kc_jwt_validation_latency_ms"
METRIC_INTROSPECTION_LATENCY = "fc_kc_introspection_latency_ms"
METRIC_REFRESH_LATENCY = "fc_kc_refresh_latency_ms"
METRIC_JWKS_FETCH_LATENCY = "fc_kc_jwks_fetch_latency_ms"
METRIC_OIDC_FETCH_LATENCY = "fc_kc_oidc_fetch_latency_ms"

METRIC_TOKEN_VALIDATION_TOTAL = "fc_kc_token_validation_total"
METRIC_TOKEN_VALIDATION_SUCCESS = "fc_kc_token_validation_success_total"
METRIC_TOKEN_VALIDATION_FAILURE = "fc_kc_token_validation_failure_total"

METRIC_TOKEN_REFRESH_TOTAL = "fc_kc_token_refresh_total"
METRIC_TOKEN_REFRESH_SUCCESS = "fc_kc_token_refresh_success_total"
METRIC_TOKEN_REFRESH_FAILURE = "fc_kc_token_refresh_failure_total"

METRIC_JWKS_CACHE_HITS = "fc_kc_jwks_cache_hits_total"
METRIC_JWKS_CACHE_MISSES = "fc_kc_jwks_cache_misses_total"

METRIC_ERRORS_TOTAL = "fc_kc_errors_total"

# Tags commonly used
TAG_ERROR_CODE = "error_code"
TAG_VALIDATION_METHOD = "method" # jwt or introspection
TAG_CLIENT_ID = "client_id"
TAG_REALM = "realm"
