"""Entry point for the Weather Analytics Dashboard API.

This module initializes the application container and creates the FastAPI app.
It's the entry point for both development (uvicorn) and production (gunicorn).
"""

import sys

from weather_analytics_dashboard.config import ConfigurationError, get_settings

# Validate settings (fail-fast)
try:
    _ = get_settings()
except ConfigurationError:
    sys.exit(1)


from weather_analytics_dashboard.presentation.api.app import create_app

# Create the FastAPI application instance
app = create_app()
