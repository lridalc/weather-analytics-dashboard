"""Unit tests for FastAPI dependency injection adapters."""

from unittest.mock import Mock

import pytest
from fastapi import Request

from weather_analytics_dashboard.bootstrap import Container
from weather_analytics_dashboard.config import Settings
from weather_analytics_dashboard.presentation.api import dependencies


@pytest.fixture
def create_mock_request():
    """Fixture that creates a mock FastAPI Request with container in app.state."""
    """
        # Create mock settings
        mock_settings = Mock(spec=Settings)
        mock_settings.environment = "test"get_container
        mock_settings.log_level = "DEBUG"

        # Create mock container with mock settings
        mock_container = Mock(spec=Container)
        mock_container.settings = mock_settings

        # Create mock state with mock container
        mock_state = Mock()
        mock_state.container = mock_container

        # Create mock app with mock state
        mock_app = Mock()
        mock_app.state = mock_state

        # Create mock request with mock app
        mock_request = Mock(spec=Request)
        mock_request.app = mock_app
    """
    mock_settings = Mock(spec=Settings, environment="test", log_level="DEBUG")
    mock_container = Mock(spec=Container, settings=mock_settings)
    mock_request = Mock()
    mock_request.app.state.container = mock_container

    return mock_request, mock_container, mock_settings


class TestDependencies:
    """Test suite for dependency injection adapters."""

    # ==================================================================================
    # TESTS FOR get_container (STATE-BASED)
    # ==================================================================================

    def test_get_container_returns_container_from_state(self, create_mock_request):
        """get_container() should retrieve container from request.app.state."""
        # Arrange & Act
        request, container, _ = create_mock_request

        result = dependencies.get_container(request)

        # Assert
        assert result is container

    def test_get_container_returns_same_container(self, create_mock_request):
        """get_container() should return same container object on multiple calls."""
        request, container, _ = create_mock_request

        result1 = dependencies.get_container(request)
        result2 = dependencies.get_container(request)

        assert result1 is container
        assert result1 is result2

    def test_get_container_with_different_requests_returns_different_containers(
        self, create_mock_request
    ):
        """Different requests may have different containers (test isolation)."""
        container1 = Mock(spec=Container)
        app1 = Mock()
        app1.state.container = container1
        request1 = Mock(spec=Request)
        request1.app = app1

        container2 = Mock(spec=Container)
        app2 = Mock()
        app2.state.container = container2
        request2 = Mock(spec=Request)
        request2.app = app2

        result1 = dependencies.get_container(request1)
        result2 = dependencies.get_container(request2)

        assert result1 is container1
        assert result2 is container2
        assert result1 is not result2

    # ==================================================================================
    # TESTS FOR get_settings (STATE-BASED)
    # ==================================================================================

    def test_get_settings_returns_settings(self, create_mock_request):
        """Should return settings from container."""
        request, container, settings = create_mock_request

        result = dependencies.get_settings(request)

        assert result is settings
        assert result.environment == "test"
        assert result.log_level == "DEBUG"

    def test_get_settings_returns_same_settings(self, create_mock_request):
        """get_settings() should return same settings object on multiple calls."""
        request, container, settings = create_mock_request

        result1 = dependencies.get_settings(request)
        result2 = dependencies.get_settings(request)

        assert result1 is settings
        assert result1 is result2

    # ==================================================================================
    # TESTS FOR TYPE ALIASES (FASTAPI INTEGRATION)
    # ==================================================================================

    def test_container_type_alias_exists(self):
        """StateContainer type alias should be defined."""
        assert hasattr(dependencies, "Container")
        assert dependencies.Container is not None

    def test_settings_type_alias_exists(self):
        """StateSettings type alias should be defined."""
        assert hasattr(dependencies, "Settings")
        assert dependencies.Settings is not None

    # ==================================================================================
    # TESTS FOR ERRORS AND LIMIT CASES
    # ==================================================================================

    def test_get_container_raises_attribute_error_if_state_container_missing(self):
        """get_container() should raise AttributeError if container is missing."""
        # Request without container in state
        request = Mock(spec=Request)
        request.app = Mock()
        request.app.state = Mock(spec=[])  # State without container

        with pytest.raises(AttributeError):
            dependencies.get_container(request)

    def test_get_settings_raises_attribute_error_if_state_container_missing(self):
        """get_container() should raise AttributeError if container is missing."""
        # Request without container in state
        request = Mock(spec=Request)
        request.app = Mock()
        request.app.state = Mock(spec=[])  # State without container

        with pytest.raises(AttributeError):
            dependencies.get_settings(request)
