"""
Smoke tests to verify application entrypoints work without crashing.

These tests ONLY verify that the application can be imported and started.
They do NOT test business logic, endpoints, or external integrations.

This file should remain minimal - only what's needed for fast CI gate.
"""


def test_cli_entrypoint_help(cli_runner):
    """Verify CLI can be invoked without import or wiring errors."""
    result = cli_runner(["--help"])
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert "Usage:" in result.stdout


def test_api_app_creation(app):
    """Verify FastAPI app can be created with full dependency graph."""
    assert app is not None
    assert app.title == "Weather Analytics Dashboard"


def test_api_root_endpoint(client):
    """Verify root endpoint responds successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Weather Analytics Dashboard API"}


def test_api_docs_available(client):
    """Verify OpenAPI docs are accessible."""
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
