"""Domain ports (interfaces) for dependency inversion.

This module defines abstract interfaces that the domain layer requires.
Infrastructure layer must provide concrete implementations of these ports.
"""

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from weather_analytics_dashboard.domain.models import WeatherData


class WeatherProviderPort(Protocol):
    """Abstract port for weather data providers.

    This interface defines what the domain layer needs from a weather provider.
    Infrastructure adapters (e.g. Open-Meteo, OpenWeatherMap) must implement this
    protocol."""

    async def get_current_weather(self, location: str) -> "WeatherData":
        """Get current weather for a location.

        Args:
            location: City or location name (e.g., "Madrid").

        Returns:
            WeatherData: Current weather data.

        Raises:
            LocationNotFoundError: If the location cannot be resolved.
            WeatherProviderUnavailableError: If the provider is temporarily unavailable.
            WeatherProviderInvalidRequestError: If the request is malformed.
            WeatherProviderRateLimitError: If the rate limit is exceeded.
        """
        ...
