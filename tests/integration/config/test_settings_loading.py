"""Integration tests for settings loading from environment and .env file."""

import pytest
from pydantic import ValidationError

from weather_analytics_dashboard.config import get_settings


class TestSettingsLoading:
    """Integration tests for settings loading mechanisms."""

    def test_settings_loads_from_dotenv_file(self, isolated_settings, tmp_path):
        """Settings should load from a .env file when present."""
        # Create a real .env file in the isolated directory
        env_file = tmp_path / ".env"
        env_file.write_text("""
API_KEY=integration-test-key-123
CACHE_TTL_WEATHER=600
ENVIRONMENT=prod
LOG_LEVEL=DEBUG
""")

        # Create settings instance (this will read the temporary .env file)
        settings = isolated_settings()

        assert settings.api_key == "integration-test-key-123"
        assert settings.cache_ttl_weather == 600
        assert settings.environment == "prod"
        assert settings.log_level == "DEBUG"

    def test_environment_variables_override_dotenv_file(
        self, isolated_settings, tmp_path, monkeypatch
    ):
        """Environment variables should take precedence over .env file values."""
        env_file = tmp_path / ".env"
        env_file.write_text("""
    API_KEY=env-file-key
    CACHE_TTL_WEATHER=100
    ENVIRONMENT=dev
    """)

        # Set environment variables with different values
        monkeypatch.setenv("API_KEY", "env-var-key")
        monkeypatch.setenv("CACHE_TTL_WEATHER", "999")
        monkeypatch.delenv("ENVIRONMENT", raising=False)

        settings = isolated_settings()

        # Environment variables should win
        assert settings.api_key == "env-var-key"
        assert settings.cache_ttl_weather == 999
        # This wasn't overridden by env var, so comes from .env
        assert settings.environment == "dev"

    def test_get_settings_returns_cached_instance(self, monkeypatch):
        """get_settings() should return the same cached instance on multiple calls."""
        monkeypatch.setenv("API_KEY", "test-cache-key")

        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2
        assert settings1.api_key == "test-cache-key"

    def test_get_settings_caches_across_module_imports(self, monkeypatch):
        """The @lru_cache decorator should cache settings across the application."""
        monkeypatch.setenv("API_KEY", "persistent-cache-key")

        # First call
        settings1 = get_settings()

        # Change environment variable (shouldn't affect cached instance)
        monkeypatch.setenv("API_KEY", "changed-key")

        # Second call should return cached instance
        settings2 = get_settings()

        assert settings1.api_key == "persistent-cache-key"
        assert settings2.api_key == "persistent-cache-key"
        assert settings1 is settings2

    def test_settings_validation_runs_on_load(self, isolated_settings, tmp_path):
        """Settings validation should run when loading from .env file."""
        env_file = tmp_path / ".env"
        env_file.write_text("""
API_KEY=
""")

        with pytest.raises(ValidationError) as exc_info:
            isolated_settings()

        errors = exc_info.value.errors()
        assert any("api_key" in e["loc"] for e in errors)

    def test_get_settings_exits_on_validation_error(self, tmp_path, monkeypatch):
        """get_settings should fail fast and exis when configuration is invalid."""
        env_file = tmp_path / ".env"
        env_file.write_text("API_KEY=")

        monkeypatch.chdir(tmp_path)

        get_settings.cache_clear()

        with pytest.raises(SystemExit) as exc_info:
            get_settings()

        assert exc_info.value.code == 1

    def test_get_settings_logs_error(self, tmp_path, monkeypatch, capsys):
        env_file = tmp_path / ".env"
        env_file.write_text("API_KEY=")

        monkeypatch.chdir(tmp_path)

        get_settings.cache_clear()

        with pytest.raises(SystemExit):
            get_settings()

        captured = capsys.readouterr()
        assert "Configuration validation failed" in captured.err
