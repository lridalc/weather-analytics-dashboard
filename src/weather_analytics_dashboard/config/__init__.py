"""Configuration module for Weather Analytics Dashboard."""

from .exceptions import ConfigurationError
from .logging import setup_logging
from .settings import Settings, get_settings

__all__ = [
    "ConfigurationError",
    "setup_logging",
    "Settings",  # For type hints and testing
    "get_settings",
]
