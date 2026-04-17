import pytest


class TestRootEndpoint:
    """Test suite for root endpoint."""

    def test_api_root_endpoint_response_format(self, client):
        """Verify root endpoint returns expected structure"""
        response = client.get("/")
        assert response.status_code == 200
        assert response.headers.get("content-type") == "application/json"
        assert response.json() == {"service": "Weather Analytics Dashboard API"}

    @pytest.mark.parametrize("method", ["post", "put", "patch", "delete"])
    def test_root_endpoint_rejects_other_methods(self, client, method):
        """Root endpoint should reject HTTP methods other than GET."""
        response = getattr(client, method)("")
        assert response.status_code == 405
