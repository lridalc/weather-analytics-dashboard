"""Entry point for the Weather Analytics Dashboard API.

This module initializes the application container and creates the FastAPI app.
It's the entry point for both development (uvicorn) and production (gunicorn).
"""
from weather_analytics_dashboard.presentation.api.app import create_app

# Create the FastAPI application instance
app = create_app()
