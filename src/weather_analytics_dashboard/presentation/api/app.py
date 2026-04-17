"""Fast API application factory."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from weather_analytics_dashboard.bootstrap import AppContainer, bootstrap
from weather_analytics_dashboard.config import Settings

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create FastAPI application with lifespan-based initialization.

    Args:
        settings: Optional settings override (useful for testing).

    Returns:
        Configured FastAPI application.
    """

    @asynccontextmanager
    async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
        """Application lifecycle management.

        Initializes the dependency container at startup and cleans up at shutdown.
        """
        logger.info("🚀 Starting Weather Analytics Dashboard...")

        # 1. Build dependency container
        container: AppContainer = bootstrap(settings)

        # 2. Attach to app state
        app_.state.container = container

        logger.info("✅ Application startup complete")

        yield

        # 3. Cleanup phase (future: close DB, HTTP clients, etc.)
        logger.info("🛑 Shutting down Weather Analytics Dashboard...")

    app = FastAPI(
        title="Weather Analytics Dashboard",
        description="Weather data service - MVP scaffold (health check only)",
        version="0.1.0",
        lifespan=lifespan,
    )

    @app.get("/")
    async def root() -> dict:
        """Root endpoint."""
        return {"service": "Weather Analytics Dashboard API"}

    return app
