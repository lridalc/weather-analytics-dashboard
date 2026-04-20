"""FastAPI dependency injection adapters."""

from typing import Annotated, cast

from fastapi import Depends, Request

from weather_analytics_dashboard.bootstrap import Container
from weather_analytics_dashboard.config import Settings


def get_container(request: Request) -> Container:
    """Get container from application state."""
    return cast(Container, request.app.state.container)


def get_settings(request: Request) -> Settings:
    """Get settings from state-based container."""
    return cast(Settings, request.app.state.container.settings)


# Type aliases for cleaner FastAPI dependency declarations
ContainerDep = Annotated[Container, Depends(get_container)]
SettingsDep = Annotated[Settings, Depends(get_settings)]
