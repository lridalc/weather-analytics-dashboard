"""Pytest configuration and shared fixtures."""

import subprocess
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def app():
    """Create FastAPI app instance once per test session."""
    from weather_analytics_dashboard.presentation.api.app import create_app

    return create_app()


@pytest.fixture
def client(app):
    """Create test client for each test."""
    return TestClient(app)


@pytest.fixture
def cli_runner():
    """Run CLI commands and return subprocess result."""
    project_root = Path(__file__).parent.parent

    def _run(args: list[str]):
        return subprocess.run(
            ["uv", "run", "weather"] + args,
            capture_output=True,
            text=True,
            cwd=project_root,
        )

    return _run


@pytest.fixture(autouse=True)
def clear_env(request, monkeypatch):
    """
    Clear all Weather Analytics Dashboard environment variables before each test.

    This fixture runs automatically (autouse=True) to ensure complete test isolation.
    No need to declare it as a test argument.
    """
    env_vars = [
        "WEATHER_API_KEY",
        "CACHE_TTL_WEATHER",
        "CACHE_TTL_GEOCODING",
        "CACHE_MAX_SIZE",
        "RETRY_MAX_ATTEMPTS",
        "RETRY_WAIT_SECONDS",
        "RATE_LIMIT_REQUESTS",
        "ENVIRONMENT",
        "LOG_LEVEL",
    ]

    # Clear environment variables
    for var in env_vars:
        monkeypatch.delenv(var, raising=False)

    if not request.node.get_closest_marker("no_test_environment"):
        # Ensure all tests run with ENVIRONMENT=test.
        # This prevents accidental use of dev/prod settings in tests.
        monkeypatch.setenv("ENVIRONMENT", "test")

    # Return control to test with clean environment
    yield


@pytest.fixture(autouse=True)
def reset_settings_cache():
    """
    Reset the get_settings() LRU cache before each test.

    This runs automatically to ensure that cached settings don't persist between tests,
    which would cause test isolation issues.
    """
    # Clean the LRU cache
    from weather_analytics_dashboard.config import get_settings

    get_settings.cache_clear()

    yield


@pytest.fixture
def isolated_settings(tmp_path, monkeypatch):
    """
    Fixture for integration tests that need real .env file isolation.

    Creates an isolated environment with:
    - Clean directory (tmp_path)
    - No pre-existing environment variables (inherits from clear_env)
    - Settings class imported after directory change
    """
    # Change to temporary directory
    monkeypatch.chdir(tmp_path)

    # Import Settings after changing directory to ensure it reads the .env from tmp_path
    from weather_analytics_dashboard.config import Settings

    # Return the Settings class, not an instance
    return Settings


@pytest.fixture
def settings(request, isolated_settings):
    """
    Provide test settings.
    """
    return isolated_settings(
        weather_api_key="test-key",
        log_level="DEBUG",
    )
