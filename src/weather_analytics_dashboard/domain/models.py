"""Domain models for weather data."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherData:
    """Current weather data for a specific location.

    This is a domain entity representing weather information at a specific point in
    time.

    Attributes:
        location: Name of the city or location.
        temperature: Temperature in Celsius.
        timestamp: When the data was collected.
    """

    location: str
    temperature: float
    timestamp: datetime
