"""Unit tests for application settings configuration."""

import pytest
from pydantic import ValidationError

from weather_analytics_dashboard.config import Settings
from weather_analytics_dashboard.config.constants import (
    DEFAULT_CACHE_MAX_SIZE,
    DEFAULT_CACHE_TTL_GEOCODING,
    DEFAULT_CACHE_TTL_WEATHER,
    DEFAULT_ENVIRONMENT,
    DEFAULT_LOG_LEVEL,
    DEFAULT_RATE_LIMIT_RPM,
    DEFAULT_REQUEST_TIMEOUT_SECONDS,
    DEFAULT_RETRY_INITIAL_WAIT_SECONDS,
    DEFAULT_RETRY_MAX_ATTEMPTS,
)


class TestSettings:
    """Test suite for Pydantic settings configuration."""

    # =========================================================================
    # ENVIRONMENT VARIABLE OVERRIDE TESTS
    # =========================================================================

    def test_all_settings_can_be_overridden(self, monkeypatch):
        """All settings should be configurable via environment variables."""
        monkeypatch.setenv("RATE_LIMIT_RPM", "30")
        monkeypatch.setenv("CACHE_TTL_WEATHER", "60")
        monkeypatch.setenv("CACHE_TTL_GEOCODING", "86400")
        monkeypatch.setenv("CACHE_MAX_SIZE", "50")
        monkeypatch.setenv("REQUEST_TIMEOUT_SECONDS", "15")
        monkeypatch.setenv("RETRY_MAX_ATTEMPTS", "5")
        monkeypatch.setenv("RETRY_INITIAL_WAIT_SECONDS", "2")
        monkeypatch.setenv("ENVIRONMENT", "prod")
        monkeypatch.setenv("LOG_LEVEL", "DEBUG")

        settings = Settings()

        assert settings.rate_limit_rpm == 30
        assert settings.cache_ttl_weather == 60
        assert settings.cache_ttl_geocoding == 86400
        assert settings.cache_max_size == 50
        assert settings.request_timeout_seconds == 15
        assert settings.retry_max_attempts == 5
        assert settings.retry_initial_wait_seconds == 2
        assert settings.environment == "prod"
        assert settings.log_level == "DEBUG"

    def test_kwargs_override_environment_variables(self, monkeypatch):
        """Direct kwargs should take precedence over environment variables."""
        monkeypatch.setenv("RATE_LIMIT_RPM", "300")
        monkeypatch.setenv("CACHE_TTL_WEATHER", "100")
        monkeypatch.setenv("ENVIRONMENT", "prod")

        settings = Settings(
            rate_limit_rpm=350,
            cache_ttl_weather=999,
            environment="test",
        )

        assert settings.rate_limit_rpm == 350
        assert settings.cache_ttl_weather == 999
        assert settings.environment == "test"
        assert settings.cache_ttl_geocoding == DEFAULT_CACHE_TTL_GEOCODING

    # =========================================================================
    # DEFAULT VALUES TESTS
    # =========================================================================

    @pytest.mark.no_test_environment
    def test_minimal_configuration_loads_with_defaults(
        self, monkeypatch, isolated_settings
    ):
        """When no optional variables are provided, all optional fields use defaults."""
        settings = isolated_settings()

        assert settings.rate_limit_rpm == DEFAULT_RATE_LIMIT_RPM
        assert settings.cache_ttl_weather == DEFAULT_CACHE_TTL_WEATHER
        assert settings.cache_ttl_geocoding == DEFAULT_CACHE_TTL_GEOCODING
        assert settings.cache_max_size == DEFAULT_CACHE_MAX_SIZE
        assert settings.request_timeout_seconds == DEFAULT_REQUEST_TIMEOUT_SECONDS
        assert settings.retry_max_attempts == DEFAULT_RETRY_MAX_ATTEMPTS
        assert settings.retry_initial_wait_seconds == DEFAULT_RETRY_INITIAL_WAIT_SECONDS
        assert settings.environment == DEFAULT_ENVIRONMENT
        assert settings.log_level == DEFAULT_LOG_LEVEL

    # =========================================================================
    # TYPE VALIDATION AND COERCION TESTS
    # =========================================================================

    def test_string_numeric_values_are_coerced_to_int(self, monkeypatch):
        """Pydantic should coerce string numbers to int."""
        monkeypatch.setenv("RATE_LIMIT_RPM", "70")
        monkeypatch.setenv("CACHE_TTL_WEATHER", "500")
        monkeypatch.setenv("CACHE_TTL_GEOCODING", "63542")
        monkeypatch.setenv("CACHE_MAX_SIZE", "200")
        monkeypatch.setenv("REQUEST_TIMEOUT_SECONDS", "15")
        monkeypatch.setenv("RETRY_MAX_ATTEMPTS", "10")
        monkeypatch.setenv("RETRY_INITIAL_WAIT_SECONDS", "3")

        settings = Settings()

        assert isinstance(settings.rate_limit_rpm, int)
        assert isinstance(settings.cache_ttl_weather, int)
        assert isinstance(settings.cache_ttl_geocoding, int)
        assert isinstance(settings.cache_max_size, int)
        assert isinstance(settings.request_timeout_seconds, int)
        assert isinstance(settings.retry_max_attempts, int)
        assert isinstance(settings.retry_initial_wait_seconds, int)
        assert settings.rate_limit_rpm == 70
        assert settings.cache_ttl_weather == 500
        assert settings.cache_ttl_geocoding == 63542
        assert settings.cache_max_size == 200
        assert settings.request_timeout_seconds == 15
        assert settings.retry_max_attempts == 10
        assert settings.retry_initial_wait_seconds == 3

    @pytest.mark.parametrize(
        ("field_name", "invalid_value"),
        [
            ("RATE_LIMIT_RPM", "1,5"),
            ("CACHE_TTL_WEATHER", "not-a-number"),
            ("CACHE_TTL_GEOCODING", "abc"),
            ("CACHE_MAX_SIZE", "12.5"),
            ("REQUEST_TIMEOUT_SECONDS", "1-5"),
            ("RETRY_MAX_ATTEMPTS", "five"),
            ("RETRY_INITIAL_WAIT_SECONDS", "one-point-five"),
        ],
        ids=lambda val: f"{val[0]}='{val[1]}'" if isinstance(val, tuple) else str(val),
    )
    def test_invalid_numeric_fields_raise_validation_error(
        self, field_name, invalid_value, monkeypatch
    ):
        """Non-integer values for numeric fields should fail validation."""
        monkeypatch.setenv(field_name, invalid_value)

        with pytest.raises(ValidationError) as exc_info:
            Settings()

        errors = exc_info.value.errors()
        assert any(field_name.lower() in e["loc"] for e in errors)

    # =========================================================================
    # BOUNDARY VALUE TESTS
    # =========================================================================

    def test_rate_limit_minimum_value_is_one(self, monkeypatch):
        """Rate limit minimum value should be 1."""
        monkeypatch.setenv("RATE_LIMIT_RPM", "1")

        settings = Settings()
        assert settings.rate_limit_rpm == 1

        monkeypatch.setenv("RATE_LIMIT_RPM", "0")
        with pytest.raises(ValidationError) as exc_info:
            Settings()

        errors = exc_info.value.errors()
        assert any("rate_limit_rpm" in e["loc"] for e in errors)

    def test_cache_ttl_zero_is_allowed(self, monkeypatch):
        """Zero TTL should be allowed (disables cache)."""
        monkeypatch.setenv("CACHE_TTL_WEATHER", "0")
        monkeypatch.setenv("CACHE_TTL_GEOCODING", "0")

        settings = Settings()

        assert settings.cache_ttl_weather == 0
        assert settings.cache_ttl_geocoding == 0

    def test_cache_max_size_minimum_value_is_one(self, monkeypatch):
        """Cache max size minimum value should be 1."""
        monkeypatch.setenv("CACHE_MAX_SIZE", "1")

        settings = Settings()
        assert settings.cache_max_size == 1

        monkeypatch.setenv("CACHE_MAX_SIZE", "0")
        with pytest.raises(ValidationError) as exc_info:
            Settings()

        errors = exc_info.value.errors()
        assert any("cache_max_size" in e["loc"] for e in errors)

    def test_request_timeout_seconds_zero_is_allowed(self, monkeypatch):
        """Zero timeout seconds should be allowed (disables timeout)."""
        monkeypatch.setenv("REQUEST_TIMEOUT_SECONDS", "0")

        settings = Settings()
        assert settings.request_timeout_seconds == 0

    def test_retry_max_attempts_zero_is_allowed(self, monkeypatch):
        """Zero retry attempts should be allowed (disables retries)."""
        monkeypatch.setenv("RETRY_MAX_ATTEMPTS", "0")

        settings = Settings()
        assert settings.retry_max_attempts == 0

    def test_retry_initial_wait_seconds_zero_is_allowed(self, monkeypatch):
        """Zero wait time should be allowed (no delay between retries)."""
        monkeypatch.setenv("RETRY_INITIAL_WAIT_SECONDS", "0")

        settings = Settings()
        assert settings.retry_initial_wait_seconds == 0

    @pytest.mark.parametrize(
        ("field_name", "negative_value"),
        [
            ("RATE_LIMIT_RPM", "-7"),
            ("CACHE_TTL_WEATHER", "-1"),
            ("CACHE_TTL_GEOCODING", "-5"),
            ("CACHE_MAX_SIZE", "-10"),
            ("REQUEST_TIMEOUT_SECONDS", "-2"),
            ("RETRY_MAX_ATTEMPTS", "-3"),
            ("RETRY_INITIAL_WAIT_SECONDS", "-2"),
        ],
        ids=lambda val: f"{val[0]}='{val[1]}'" if isinstance(val, tuple) else str(val),
    )
    def test_negative_values_raise_validation_error(
        self, field_name, negative_value, monkeypatch
    ):
        """Negative values should fail validation for constrained fields."""
        monkeypatch.setenv(field_name, negative_value)

        with pytest.raises(ValidationError) as exc_info:
            Settings()

        errors = exc_info.value.errors()
        assert any(field_name.lower() in e["loc"] for e in errors)

    # =========================================================================
    # ENVIRONMENT VALIDATION TESTS
    # =========================================================================

    @pytest.mark.parametrize("valid_env", ["dev", "test", "prod"])
    def test_valid_environments_are_accepted(self, valid_env, monkeypatch):
        """'dev', 'test', and 'prod' should be valid environment values."""
        monkeypatch.setenv("ENVIRONMENT", valid_env)

        settings = Settings()
        assert settings.environment == valid_env

    @pytest.mark.parametrize(
        "invalid_env",
        ["staging", "production", "DEVELOPMENT", "Dev", "PROD", "", " "],
        ids=lambda x: f"'{x}'" if x.strip() else f"'{repr(x)}'",
    )
    def test_invalid_environment_raises_validation_error(
        self, invalid_env, monkeypatch
    ):
        """Only 'dev', 'test', 'prod' are valid environments (case-sensitive)."""
        monkeypatch.setenv("ENVIRONMENT", invalid_env)

        with pytest.raises(ValidationError) as exc_info:
            Settings()

        errors = exc_info.value.errors()
        assert any("environment" in e["loc"] for e in errors)

    # =========================================================================
    # LOG LEVEL VALIDATION TESTS
    # =========================================================================

    @pytest.mark.parametrize(
        "valid_level", ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    )
    def test_valid_log_levels_are_accepted(self, valid_level, monkeypatch):
        """Standard Python log levels should be valid."""
        monkeypatch.setenv("LOG_LEVEL", valid_level)

        settings = Settings()
        assert settings.log_level == valid_level

    @pytest.mark.parametrize(
        "invalid_level",
        ["VERBOSE", "WARN", "debug", "info", "warning", "", " ", "TRACE"],
        ids=lambda x: f"'{x}'" if x.strip() else f"'{repr(x)}'",
    )
    def test_invalid_log_level_raises_validation_error(
        self, invalid_level, monkeypatch
    ):
        """Only standard Python log levels are valid (case-sensitive)."""
        monkeypatch.setenv("LOG_LEVEL", invalid_level)

        with pytest.raises(ValidationError) as exc_info:
            Settings()

        errors = exc_info.value.errors()
        assert any("log_level" in e["loc"] for e in errors)

    # =========================================================================
    # EDGE CASE TESTS
    # =========================================================================

    def test_extra_environment_variables_are_ignored(self, monkeypatch):
        """Unknown environment variables should be ignored (extra='ignore')."""
        monkeypatch.setenv("UNKNOWN_VARIABLE", "should-be-ignored")
        monkeypatch.setenv("ANOTHER_UNKNOWN", "also-ignored")

        settings = Settings()

        assert not hasattr(settings, "UNKNOWN_VARIABLE")
        assert not hasattr(settings, "ANOTHER_UNKNOWN")

    @pytest.mark.no_test_environment
    def test_settings_can_be_created_with_kwargs_without_env(self):
        """Settings should be instantiable via kwargs (bypassing environment)."""
        settings = Settings(
            cache_ttl_weather=999,
            environment="test",
        )

        assert settings.cache_ttl_weather == 999
        assert settings.environment == "test"
        assert settings.cache_ttl_geocoding == DEFAULT_CACHE_TTL_GEOCODING

    def test_settings_model_dump_returns_dict(self, monkeypatch):
        """Settings should be serializable to dict in Pydantic v2."""
        monkeypatch.setenv("RATE_LIMIT_RPM", "20")
        monkeypatch.setenv("CACHE_TTL_WEATHER", "999")

        settings = Settings()
        data = settings.model_dump()

        assert isinstance(data, dict)
        assert "rate_limit_rpm" in data
        assert data["rate_limit_rpm"] == 20
        assert "cache_ttl_weather" in data
        assert data["cache_ttl_weather"] == 999
