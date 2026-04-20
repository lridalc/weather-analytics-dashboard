"""Domain-specific exceptions."""


class DomainError(Exception):
    """Base class for all domain exceptions.

    This allows catching any domain-specific error with a single except clause.
    """

    pass


class WeatherProviderError(DomainError):
    """Base class for weather provider related errors.

    Infrastructure adapters should raise specific subclasses for this exception when
    internal API calls fail."""

    pass


class WeatherProviderUnavailableError(WeatherProviderError):
    """Raised when the weather provider is temporarily unavailable.

    This includes network timeouts, 5xx responses, and retry exhaustion.
    Infrastructure adapters should raise this after retries are exhausted.
    """

    def __init__(self, details: str = "Service temporarily unavailable") -> None:
        super().__init__(details)


class WeatherProviderRateLimitError(WeatherProviderError):
    """Raised when the weather provider rate limit has been exceeded."""

    def __init__(self, details: str = "Rate limit exceeded") -> None:
        super().__init__(details)


class WeatherProviderInvalidRequestError(WeatherProviderError):
    """Raised when the request to the weather provider is malformed.

    This includes 4xx errors other than location not found (e.g., invalid API key,
    missing parameters). Unlike provider unavailable, retrying will not help.
    """

    def __init__(self, details: str = "Invalid request") -> None:
        super().__init__(details)


class LocationNotFoundError(WeatherProviderError):
    """Raised when a location was not found.

    This is a domain exception. Infrastructure adapters should catch provider-specific
    errors and convert them to this domain exception."""

    def __init__(self, location: str) -> None:
        self.location = location
        super().__init__(f"Location not found: {location}")
