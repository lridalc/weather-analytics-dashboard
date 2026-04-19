"""Default configuration constants for Weather Analytics Dashboard."""

from typing import Literal

# ======================================================================================
# RATE LIMITING DEFAULTS
# ======================================================================================

DEFAULT_RATE_LIMIT_RPM = 250  # Safety margin for geocoding with free tier (600 RPM)

# ======================================================================================
# CACHING DEFAULTS
# ======================================================================================

DEFAULT_CACHE_TTL_WEATHER = 300  # 5 minutes
DEFAULT_CACHE_TTL_GEOCODING = 604800  # 7 days
DEFAULT_CACHE_MAX_SIZE = 100

# ======================================================================================
# RESILIENCY DEFAULTS
# ======================================================================================

DEFAULT_REQUEST_TIMEOUT_SECONDS = 10
DEFAULT_RETRY_MAX_ATTEMPTS = 3
DEFAULT_RETRY_INITIAL_WAIT_SECONDS = 1

# ======================================================================================
# OBSERVABILITY DEFAULTS
# ======================================================================================

type Environment = Literal["dev", "test", "prod"]
type LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

DEFAULT_ENVIRONMENT: Environment = "dev"
DEFAULT_LOG_LEVEL: LogLevel = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
