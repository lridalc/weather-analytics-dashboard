"""Integration tests for the /health endpoint."""


class TestHealthEndpoint:
    """Test suite for health check endpoint."""

    def test_health_endpoint_returns_200_status(self, client):
        """GET /health should return HTTP 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_json_content_type(self, client):
        """GET /health should return application/json content-type header."""
        response = client.get("/health")
        assert response.headers["Content-Type"] == "application/json"

    def test_health_endpoint_response_structure(self, client):
        """GET /health response should contain required status field."""
        response = client.get("/health")
        assert "status" in response.json()

    def test_health_endpoint_status_field_is_string(self, client):
        """GET /health status field should be string."""
        response = client.get("/health")
        assert isinstance(response.json()["status"], str)

    def test_health_endpoint_returns_healthy_status(self, client):
        """GET /health should return healthy status."""
        response = client.get("/health")
        assert response.json() == {"status": "healthy"}

    def test_health_endpoint_accepts_get_only(self, client):
        """GET /health should only accept GET requests."""
        # POST should fail
        response = client.post("/health")
        assert response.status_code == 405

        # PUT should fail
        response = client.put("/health")
        assert response.status_code == 405

        # DELETE should fail
        response = client.delete("/health")
        assert response.status_code == 405

    def test_health_endpoint_always_returns_healthy_status(self, client):
        """GET /health should always return healthy status when service is running."""
        for _ in range(10):
            response = client.get("/health")
            assert response.json()["status"] == "healthy"
