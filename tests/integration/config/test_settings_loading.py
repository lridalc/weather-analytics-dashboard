"""Integration tests for settings loading from environment and .env file."""

import pytest
from pydantic import ValidationError

from weather_analytics_dashboard.config import ConfigurationError, get_settings


class TestSettingsLoading:
    """Integration tests for settings loading mechanisms."""

    @pytest.mark.no_test_environment
    def test_settings_loads_from_dotenv_file(self, isolated_settings, tmp_path):
        """Settings should load from a .env file when present."""
        # Create a real .env file in the isolated directory
        env_file = tmp_path / ".env"
        env_file.write_text("""
RATE_LIMIT_RPM = 200
CACHE_TTL_WEATHER=600
ENVIRONMENT=prod
LOG_LEVEL=DEBUG
""")

        # Create settings instance (this will read the temporary .env file)
        settings = isolated_settings()

        assert settings.rate_limit_rpm == 200
        assert settings.cache_ttl_weather == 600
        assert settings.environment == "prod"
        assert settings.log_level == "DEBUG"

    @pytest.mark.no_test_environment
    def test_environment_variables_override_dotenv_file(
        self, isolated_settings, tmp_path, monkeypatch
    ):
        """Environment variables should take precedence over .env file values."""
        env_file = tmp_path / ".env"
        env_file.write_text("""
RATE_LIMIT_RPM = 300
CACHE_TTL_WEATHER=100
ENVIRONMENT=dev
    """)

        # Set environment variables with different values
        monkeypatch.setenv("RATE_LIMIT_RPM", "100")
        monkeypatch.setenv("CACHE_TTL_WEATHER", "999")

        settings = isolated_settings()

        # Environment variables should win
        assert settings.rate_limit_rpm == 100
        assert settings.cache_ttl_weather == 999
        # This wasn't overridden by env var, so comes from .env
        assert settings.environment == "dev"

    def test_get_settings_returns_cached_instance(self, monkeypatch):
        """get_settings() should return the same cached instance on multiple calls."""
        monkeypatch.setenv("RATE_LIMIT_RPM", "150")

        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2
        assert settings1.rate_limit_rpm == 150

    def test_get_settings_caches_across_module_imports(self, monkeypatch):
        """The @lru_cache decorator should cache settings across the application."""
        monkeypatch.setenv("RATE_LIMIT_RPM", "50")

        # First call
        settings1 = get_settings()

        # Change environment variable (shouldn't affect cached instance)
        monkeypatch.setenv("RATE_LIMIT_RPM", "70")

        # Second call should return cached instance
        settings2 = get_settings()

        assert settings1.rate_limit_rpm == 50
        assert settings2.rate_limit_rpm == 50
        assert settings1 is settings2

    def test_settings_validation_runs_on_load(self, isolated_settings, tmp_path):
        """Settings validation should run when loading from .env file."""
        env_file = tmp_path / ".env"
        env_file.write_text("""
RATE_LIMIT_RPM=-20
""")

        with pytest.raises(ValidationError) as exc_info:
            isolated_settings()

        errors = exc_info.value.errors()
        assert any("rate_limit_rpm" in e["loc"] for e in errors)

    def test_get_settings_raises_configuration_error_on_validation_failure(
        self, tmp_path, monkeypatch
    ):
        """get_settings should raise ConfigurationError when validation fails."""
        env_file = tmp_path / ".env"
        env_file.write_text("RATE_LIMIT_RPM=-20")

        monkeypatch.chdir(tmp_path)

        get_settings.cache_clear()

        with pytest.raises(ConfigurationError) as exc_info:
            get_settings()

        assert exc_info.value.__cause__ is not None
        assert isinstance(exc_info.value.__cause__, ValidationError)

    def test_get_settings_logs_error_on_validation_failure(
        self, tmp_path, monkeypatch, capsys
    ):
        """get_settings should log error details when validation fails."""
        env_file = tmp_path / ".env"
        env_file.write_text("RATE_LIMIT_RPM=-20")

        monkeypatch.chdir(tmp_path)

        get_settings.cache_clear()

        with pytest.raises(ConfigurationError):
            get_settings()

        captured = capsys.readouterr()
        assert "Configuration validation failed" in captured.err
        assert "RATE_LIMIT_RPM" in captured.err
