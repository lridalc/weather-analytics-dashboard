"""FastAPI dependency injection adapters."""

from functools import lru_cache
from typing import Annotated, cast

from fastapi import Depends, Request

from weather_analytics_dashboard.bootstrap import AppContainer, bootstrap
from weather_analytics_dashboard.config import Settings


@lru_cache(maxsize=1)
def get_container() -> AppContainer:
    """Get or create the application container singleton.

    This function is cached to ensure bootstrap() runs only once
    per application lifecycle when used outside of lifespan.
    """
    return bootstrap()


def get_container_from_state(request: Request) -> AppContainer:
    """Get container from application state.

    Preferred method when using lifespan-based initialization.
    """
    return cast(AppContainer, request.app.state.container)


def get_settings_from_state(request: Request) -> Settings:
    """Get settings from state-based container."""
    container: AppContainer = request.app.state.container
    return container.settings


# Type aliases for cleaner FastAPI dependency declarations
Container = Annotated[AppContainer, Depends(get_container)]
StateContainer = Annotated[AppContainer, Depends(get_container_from_state)]
StateSettings = Annotated[Settings, Depends(get_settings_from_state)]
