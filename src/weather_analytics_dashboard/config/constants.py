"""Default configuration constants for Weather Analytics Dashboard."""

from typing import Literal, TypeAlias

# =============================================================================
# CACHING DEFAULTS
# =============================================================================

DEFAULT_CACHE_TTL_WEATHER = 300  # 5 minutes
DEFAULT_CACHE_TTL_GEOCODING = 604800  # 7 days
DEFAULT_CACHE_MAX_SIZE = 100

# =============================================================================
# RESILIENCY DEFAULTS
# =============================================================================

DEFAULT_RETRY_MAX_ATTEMPTS = 3
DEFAULT_RETRY_WAIT_SECONDS = 1

# =============================================================================
# RATE LIMITING DEFAULTS
# =============================================================================

DEFAULT_RATE_LIMIT_REQUESTS = 55  # Safety margin for OpenWeatherMap free tier (60)

# =============================================================================
# OBSERVABILITY DEFAULTS
# =============================================================================

Environment: TypeAlias = Literal["dev", "test", "prod"]
LogLevel: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

DEFAULT_ENVIRONMENT: Environment = "dev"
DEFAULT_LOG_LEVEL: LogLevel = "INFO"