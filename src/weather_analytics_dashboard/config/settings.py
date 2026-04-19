"""Application settings configuration using Pydantic Settings."""

import logging
import sys
from functools import lru_cache

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import (
    DEFAULT_CACHE_MAX_SIZE,
    DEFAULT_CACHE_TTL_GEOCODING,
    DEFAULT_CACHE_TTL_WEATHER,
    DEFAULT_ENVIRONMENT,
    DEFAULT_LOG_LEVEL,
    DEFAULT_RATE_LIMIT_RPM,
    DEFAULT_REQUEST_TIMEOUT_SECONDS,
    DEFAULT_RETRY_INITIAL_WAIT_SECONDS,
    DEFAULT_RETRY_MAX_ATTEMPTS,
    LOG_FORMAT,
    Environment,
    LogLevel,
)
from .exceptions import ConfigurationError


class Settings(BaseSettings):
    """Weather Analytics Dashboard configuration settings.

    All settings can be configured via environment variables or .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # =========================================================================
    # RATE LIMITING
    # =========================================================================

    rate_limit_rpm: int = Field(
        default=DEFAULT_RATE_LIMIT_RPM,
        title="Rate limit requests",
        description="Max requests per minute",
        ge=1,
    )

    # =========================================================================
    # CACHING
    # =========================================================================

    cache_ttl_weather: int = Field(
        default=DEFAULT_CACHE_TTL_WEATHER,
        title="Weather data cache TTL",
        description="Weather data cache TTL in seconds (0 to disable)",
        ge=0,
    )

    cache_ttl_geocoding: int = Field(
        default=DEFAULT_CACHE_TTL_GEOCODING,
        title="Geocoding data cache TTL",
        description="Geocoding data cache TTL in seconds (0 to disable)",
        ge=0,
    )

    cache_max_size: int = Field(
        default=DEFAULT_CACHE_MAX_SIZE,
        title="Cache max size",
        description="Maximum number of entries in the cache (FIFO eviction)",
        ge=1,
    )

    # =========================================================================
    # RESILIENCY
    # =========================================================================

    request_timeout_seconds: int = Field(
        default=DEFAULT_REQUEST_TIMEOUT_SECONDS,
        title="Request max timeout seconds",
        description="Max timeout seconds for a single HTTP request/response",
        ge=0,
    )

    retry_max_attempts: int = Field(
        default=DEFAULT_RETRY_MAX_ATTEMPTS,
        title="Retry max attempts",
        description="Max retry attempts for transient HTTP failures (0 to disable)",
        ge=0,
    )

    retry_initial_wait_seconds: int = Field(
        default=DEFAULT_RETRY_INITIAL_WAIT_SECONDS,
        title="Retry wait seconds",
        description="Initial wait time between retries in seconds (exponential backoff,"
        "0 for no delay)",
        ge=0,
    )

    # =========================================================================
    # OBSERVABILITY
    # =========================================================================

    environment: Environment = Field(
        default=DEFAULT_ENVIRONMENT,
        title="Environment",
        description="Execution environment",
    )

    log_level: LogLevel = Field(
        default=DEFAULT_LOG_LEVEL,
        title="Log level",
        description="Logging verbosity level",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: Cached application settings.

    Raises:
        ValidationError: If required settings are missing or invalid.
    """
    # Configure minimal logging for fatal configuration errors
    logging.basicConfig(
        level=logging.CRITICAL,
        format=LOG_FORMAT,
        stream=sys.stderr,
        force=True,
    )

    logger = logging.getLogger(__name__)

    try:
        return Settings()  # type: ignore[call-arg]
    except ValidationError as e:
        # Log the fatal error
        logger.critical("=" * 60)
        logger.critical("❌ FATAL: Configuration validation failed")
        logger.critical("=" * 60)
        logger.critical("Please fix the following errors in your .env file:")

        for error in e.errors():
            loc = " -> ".join(str(loc).upper() for loc in error["loc"])
            msg = error["msg"]
            logger.critical(f"  • {loc}: {msg}")

        logger.critical("=" * 60)
        logger.critical("💡 Tip: Copy .env.example to .env")
        logger.critical("=" * 60)

        raise ConfigurationError() from e
