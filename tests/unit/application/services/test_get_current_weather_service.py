"""Unit tests for GetCurrentWeatherService."""

from unittest.mock import AsyncMock

import pytest
from weather_analytics_dashboard.application.services.get_current_weather import (
    GetCurrentWeatherService,
)
from weather_analytics_dashboard.domain.exceptions import LocationNotFoundError
from weather_analytics_dashboard.domain.models import WeatherData


class TestGetCurrentWeatherService:
    """Test suite for GetCurrentWeatherService use case."""

    @pytest.fixture
    def mock_weather_provider(self):
        """Create a mock weather provider port."""
        mock = AsyncMock()
        mock.get_current = AsyncMock()
        return mock

    @pytest.mark.asyncio
    async def test_execute_returns_weather_data_for_valid_location(
        self, mock_weather_provider
    ):
        """
        Service should return weather data when provider returns data (happy path).
        """
        # Arrange
        expected_data = WeatherData(
            location="Madrid",
            temperature=22.0,
            timestamp="2026-04-20T12:00:00Z",
        )
        mock_weather_provider.get_current.return_value = expected_data

        service = GetCurrentWeatherService(mock_weather_provider)

        # Act
        result = await service.execute("Madrid")

        # Assert
        assert result == expected_data
        mock_weather_provider.get_current.assert_awaited_once_with("Madrid")

    @pytest.mark.asyncio
    async def test_execute_propagates_location_not_found_error(
        self, mock_weather_provider
    ):
        """Service should propagate LocationNotFoundError when provider raises it."""
        # Arrange
        mock_weather_provider.get_current.side_effect = LocationNotFoundError(
            "UnknownCity"
        )

        service = GetCurrentWeatherService(mock_weather_provider)

        # Act & Assert
        with pytest.raises(LocationNotFoundError) as exc_info:
            await service.execute("UnknownCity")

        assert str(exc_info.value) == "UnknownCity"
        mock_weather_provider.get_current.assert_awaited_once_with("UnknownCity")
