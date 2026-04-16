"""Logging configuration for Weather Analytics Dashboard."""

import logging
import sys

from .constants import LOG_FORMAT
from .settings import Settings


def setup_logging(settings: Settings) -> None:
    """Configure application logging.

    In test environment, we avoid force=True to preserve pytest's caplog fixture.
    In dev/prod, we force configuration to ensure consistent logging setup.

    Args:
        settings: Settings instance to use settings.log_level.
    """
    level = settings.log_level

    # In tests, let pytest handle logging configuration
    if settings.environment == "test":
        # Just set the level on the root logger that pytest already configured
        logging.getLogger().setLevel(level)
    else:
        # Configure root logger
        logging.basicConfig(
            level=level,
            format=LOG_FORMAT,
            stream=sys.stdout,
            force=True,
        )

    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    # Log startup information
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {level}")
