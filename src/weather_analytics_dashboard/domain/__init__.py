"""Domain layer for Weather Analytics Dashboard."""

from .exceptions import (
    LocationNotFoundError,
    WeatherProviderError,
    WeatherProviderInvalidRequestError,
    WeatherProviderRateLimitError,
    WeatherProviderUnavailableError,
)
from .models import WeatherData
from .ports import WeatherProviderPort

__all__ = [
    "WeatherData",
    "WeatherProviderPort",
    "WeatherProviderError",
    "WeatherProviderUnavailableError",
    "WeatherProviderRateLimitError",
    "WeatherProviderInvalidRequestError",
    "LocationNotFoundError",
]
