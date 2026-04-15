"""Composition root for dependency injection."""

import logging
from dataclasses import dataclass

from weather_analytics_dashboard.config import Settings, get_settings, setup_logging

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AppContainer:
    """Container holding all application dependencies.

    This is an immutable data holder. All dependencies are built in the bootstrap
    function and stored here. Constructor injection is used throughout the application.

    Attributes:
        settings: Application configuration

    More attributes will be added in future phases.
    """

    settings: Settings

    # Infrastructure layer (to be added in future phases)

    # Application layer (to be added in future phases)


def bootstrap(settings: Settings | None = None) -> AppContainer:
    """Build the application dependency graph.

    This is the COMPOSITION ROOT. All object construction happens here.
    The function is pure and side effect free (except for logging setup, which is
    idempotent). This makes it perfect for testing.

    Args:
        settings: Optional Settings override for testing.
                 If None, loads from environment/.env file.

    Returns:
        AppContainer: Fully constructed dependency container.

    Raises:
        SystemExit: If configuration validation fails (handled in get_settings).
    """
    # 1. Load configuration (fails fast if invalid)
    if settings is None:
        settings = get_settings()

    # 2. Configure logging (idempotent - safe to call multiple times)
    setup_logging(settings)

    logger.info("Bootstrapping Weather Analytics Dashboard...")

    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Log level: {settings.log_level}")
    logger.info("Configuration loaded successfully")

    # 3. Build Infrastructure Layer (in future phases)

    # 4. Build Domain Adapters (in future phases)

    # 5. Build Repositories (in future phases)

    # 6. Build Application Services (in future phases)

    # 7. Assemble and return container
    container = AppContainer(
        settings=settings,
    )

    logger.info("✅ Dependency graph built successfully")
    return container
