"""Application settings configuration using Pydantic Settings."""

from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from weather_analytics_dashboard.config.constants import (
    DEFAULT_CACHE_MAX_SIZE,
    DEFAULT_CACHE_TTL_GEOCODING,
    DEFAULT_CACHE_TTL_WEATHER,
    DEFAULT_RATE_LIMIT_REQUESTS,
    DEFAULT_RETRY_MAX_ATTEMPTS,
    DEFAULT_RETRY_WAIT_SECONDS,
    DEFAULT_ENVIRONMENT,
    DEFAULT_LOG_LEVEL,
    Environment,
    LogLevel,
)


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

    api_key: str = Field(
        ...,
        min_length=1,
        description="OpenWeatherMap API key (required)",
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
        description="Initial wait time between retries in seconds (exponential backoff, 0 for no delay)",
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

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate that API key is not empty or whitespace only."""
        if not v or not v.strip():
            raise ValueError("API_KEY cannot be empty or whitespace only")
        return v.strip()
