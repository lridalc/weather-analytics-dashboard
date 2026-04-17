"""Integration tests for the /health endpoint."""

import pytest


class TestHealthEndpoint:
    """Test suite for health check endpoint."""

    def test_health_endpoint_returns_200_status_code(self, client):
        """GET /health should return HTTP 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json_content_type(self, client):
        """GET /health should return application/json content-type header."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"

    def test_health_endpoint_response_content(self, client):
        """GET /health should return exact expected response."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_health_endpoint_idempotent(self, client):
        """GET /health should return consistent results on repeated calls."""
        first_response = client.get("/health")
        assert first_response.status_code == 200
        first = first_response.json()

        for _ in range(5):
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json() == first

    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    def test_health_endpoint_accepts_get_only(self, client, method):
        """/health endpoint should reject HTTP methods other than GET."""
        response = getattr(client, method)("/health")
        assert response.status_code == 405
