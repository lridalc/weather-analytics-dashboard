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
