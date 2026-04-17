"""
Smoke tests to verify application entrypoints work without crashing.

These tests ONLY verify that the application can be imported and started.
They do NOT test business logic, endpoints, or external integrations.

This file should remain minimal - only what's needed for fast CI gate.
"""


class TestSmoke:
    def test_cli_entrypoint_no_args(self, cli_runner):
        """Verify CLI entrypoint works without crashing."""
        result = cli_runner([])
        # check=True already validates returncode
        # Explicit assert improves readability
        assert result.returncode == 0

    def test_cli_entrypoint_help(self, cli_runner):
        """Verify CLI --help entrypoint works without crashing."""
        result = cli_runner(["--help"])
        # check=True already validates returncode
        # Explicit assert improves readability
        assert result.returncode == 0

    def test_api_app_creation(self, app):
        """Verify FastAPI app can be created with full dependency graph."""
        assert app is not None
        assert app.title == "Weather Analytics Dashboard"

    def test_api_root_endpoint(self, client):
        """Verify Root endpoint responds successfully."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()

    def test_api_health_endpoint(self, client):
        """Verify Health endpoint responds successfully."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()

    def test_api_docs_available(self, client):
        """Verify OpenAPI docs are accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert "openapi" in response.json()
