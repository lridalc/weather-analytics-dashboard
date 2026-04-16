"""Application settings configuration using Pydantic Settings."""

import logging
import sys

from anyio.functools import lru_cache
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import (
    DEFAULT_CACHE_MAX_SIZE,
    DEFAULT_CACHE_TTL_GEOCODING,
    DEFAULT_CACHE_TTL_WEATHER,
    DEFAULT_ENVIRONMENT,
    DEFAULT_LOG_LEVEL,
    DEFAULT_RATE_LIMIT_REQUESTS,
    DEFAULT_RETRY_MAX_ATTEMPTS,
    DEFAULT_RETRY_WAIT_SECONDS,
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
        validate_default=True,
    )

    # =========================================================================
    # API KEY (REQUIRED)
    # =========================================================================

    weather_api_key: str = Field(
        ...,
        description="API key (required)",
    )

    # =========================================================================
    # CACHING
    # =========================================================================

    cache_ttl_weather: int = Field(
        default=DEFAULT_CACHE_TTL_WEATHER,
        ge=0,
        description="Weather data cache TTL in seconds (0 to disable)",
    )

    cache_ttl_geocoding: int = Field(
        default=DEFAULT_CACHE_TTL_GEOCODING,
        ge=0,
        description="Geocoding data cache TTL in seconds (0 to disable)",
    )

    cache_max_size: int = Field(
        default=DEFAULT_CACHE_MAX_SIZE,
        ge=1,
        description="Maximum number of entries in the cache (FIFO eviction)",
    )

    # =========================================================================
    # RESILIENCY
    # =========================================================================

    retry_max_attempts: int = Field(
        default=DEFAULT_RETRY_MAX_ATTEMPTS,
        ge=0,
        description="Max retry attempts for transient HTTP failures (0 to disable)",
    )

    retry_wait_seconds: int = Field(
        default=DEFAULT_RETRY_WAIT_SECONDS,
        ge=0,
        description="Initial wait time between retries in seconds (exponential backoff,"
        "0 for no delay)",
    )

    # =========================================================================
    # RATE LIMITING
    # =========================================================================

    rate_limit_requests: int = Field(
        default=DEFAULT_RATE_LIMIT_REQUESTS,
        ge=1,
        description="Max requests per minute",
    )

    # =========================================================================
    # OBSERVABILITY
    # =========================================================================

    environment: Environment = Field(
        default=DEFAULT_ENVIRONMENT,
        description="Execution environment",
    )

    log_level: LogLevel = Field(
        default=DEFAULT_LOG_LEVEL,
        description="Logging verbosity level",
    )

    # =========================================================================
    # VALIDATORS
    # =========================================================================

    @field_validator("weather_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate that API key is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError("WEATHER_API_KEY cannot be empty or whitespace only")
        return v.strip()


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
        logger.critical("💡 Tip: Copy .env.example to .env and add your API key")
        logger.critical("=" * 60)

        raise ConfigurationError() from e
