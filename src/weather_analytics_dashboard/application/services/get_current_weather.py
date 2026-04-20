"""Get current weather use case."""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from weather_analytics_dashboard.domain import WeatherData, WeatherProviderPort

logger = logging.getLogger(__name__)


class GetCurrentWeatherService:
    """Orchestrates retrieving current weather for a location.

    This service follows the Single Responsibility Principle:
    it only orchestrates the flow between presentation and domain,
    without containing business logic itself.
    """

    def __init__(self, weather_provider: "WeatherProviderPort") -> None:
        """Initialize the service with a weather provider.

        Args:
            weather_provider: Port implementation for weather data retrieval.
        """
        self._weather_provider = weather_provider

    async def execute(self, location: str) -> "WeatherData":
        """Execute the use case to get current weather.

        Args:
            location: City or location name (e.g., "Madrid").

        Returns:
            WeatherData: Current weather data for the location.

        Raises:
            WeatherProviderUnavailableError: If the provider is temporarily unavailable.
            WeatherProviderRateLimitError: If the rate limit is exceeded.
            WeatherProviderInvalidRequestError: If the request is malformed.
            LocationNotFoundError: If the location cannot be resolved.
        """

        logger.info(f"Getting current weather for location: {location}")

        # Delegate to the provider - no business logic here
        weather_data = await self._weather_provider.get_current_weather(location)

        logger.info(
            "Successfully retrieved current weather for %s: %.1fºC",
            location,
            weather_data.temperature,
        )

        return weather_data
