"""Smoke tests to verify basic application bootstrapping."""


def test_cli_entrypoint_help(cli_runner):
    """Verify CLI can be invoked without import errors."""
    result = cli_runner(["--help"])
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert "Usage:" in result.stdout


def test_api_app_creation(app):
    """Verify FastAPI app can be created without errors."""
    assert app is not None
    assert app.title == "Weather Analytics Dashboard"


def test_api_root_endpoint(client):
    """Verify root endpoint responds."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_api_docs_available(client):
    """Verify OpenAPI docs are accessible."""
    response = client.get("/docs")
    assert response.status_code == 200

    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()