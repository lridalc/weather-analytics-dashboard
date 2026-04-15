"""Logging configuration for Weather Analytics Dashboard."""

import logging
import sys

from weather_analytics_dashboard.config import LOG_FORMAT
from weather_analytics_dashboard.config.settings import Settings


def setup_logging(settings: Settings) -> None:
    """Configure application logging.

    Args:
        settings: Settings instance to use settings.log_level.
    """
    level = settings.log_level

    # Configure root logger
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        stream=sys.stdout,
        force=True,  # Override any existing configuration
    )

    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    # Log startup information
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {level}")
