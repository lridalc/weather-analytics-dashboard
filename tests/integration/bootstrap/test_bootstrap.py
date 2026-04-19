"""
Integration tests for bootstrap composition root.

These tests validate that the application is correctly wired together:

- Bootstrap acts as the composition root
- Settings are correctly injected or loaded
- No mutation of input objects occurs
- Basic observability (logging) is triggered

We explicitly avoid testing:
- Logging internals (covered elsewhere)
- Settings validation (covered elsewhere)
- Caching behavior (covered elsewhere)
"""

import pytest

from weather_analytics_dashboard.bootstrap import AppContainer, bootstrap


class TestBootstrap:
    """Integration tests for application bootstrap."""

    # =========================================================================
    # CORE BEHAVIOR
    # =========================================================================

    def test_bootstrap_returns_app_container(self, settings):
        """bootstrap() should return a valid AppContainer."""
        container = bootstrap(settings=settings)

        assert isinstance(container, AppContainer)

    def test_bootstrap_uses_provided_settings(self, settings):
        """bootstrap() should use explicitly provided settings."""
        container = bootstrap(settings=settings)

        assert container.settings is settings

    def test_bootstrap_loads_settings_when_not_provided(self, monkeypatch):
        """bootstrap() should load settings from environment if not provided."""
        monkeypatch.setenv("RATE_LIMIT_RPM", "1")

        container = bootstrap()

        assert container.settings.rate_limit_rpm == 1

    def test_bootstrap_accepts_none_settings(self, monkeypatch):
        """bootstrap(settings=None) should behave like no settings provided."""
        monkeypatch.setenv("RATE_LIMIT_RPM", "1")

        container = bootstrap(settings=None)

        assert container.settings.rate_limit_rpm == 1

    def test_bootstrap_returns_new_container_each_call(self, settings):
        """Each bootstrap call should return a new container instance."""
        container1 = bootstrap(settings=settings)
        container2 = bootstrap(settings=settings)

        assert container1 is not container2

    def test_bootstrap_does_not_mutate_settings(self, settings):
        """bootstrap() must not modify the provided Settings object."""
        original_rate_limit_rpm = settings.rate_limit_rpm
        original_log_level = settings.log_level

        bootstrap(settings=settings)

        assert settings.rate_limit_rpm == original_rate_limit_rpm
        assert settings.log_level == original_log_level

    def test_bootstrap_is_deterministic(self, settings):
        """bootstrap() should behave deterministically for the same input."""
        container1 = bootstrap(settings=settings)
        container2 = bootstrap(settings=settings)

        assert container1.settings.environment == container2.settings.environment
        assert container1.settings.log_level == container2.settings.log_level

    # =========================================================================
    # LOGGING (INTEGRATION SIGNAL ONLY)
    # =========================================================================

    def test_bootstrap_emits_startup_logs(self, settings, caplog):
        """bootstrap() should emit basic startup logs."""
        bootstrap(settings=settings)

        messages = [record.message for record in caplog.records]

        assert any("Bootstrapping" in msg for msg in messages)
        assert any("Configuration loaded successfully" in msg for msg in messages)

    # =========================================================================
    # MINIMAL DEPENDENCY GRAPH
    # =========================================================================

    def test_bootstrap_builds_valid_container(self, settings):
        """bootstrap() should construct a valid dependency container."""
        container = bootstrap(settings=settings)

        assert hasattr(container, "settings")
        assert container.settings is not None

    # =========================================================================
    # ERROR PROPAGATION
    # =========================================================================

    def test_bootstrap_propagates_configuration_errors(self, monkeypatch):
        # Invalid RATE_LIMIT_RPM
        monkeypatch.setenv("RATE_LIMIT_RPM", "-1")

        """bootstrap() should propagate configuration errors."""
        from weather_analytics_dashboard.config import ConfigurationError

        with pytest.raises(ConfigurationError):
            bootstrap()
