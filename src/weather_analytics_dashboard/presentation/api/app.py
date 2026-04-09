from fastapi import FastAPI

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title="Weather Analytics Dashboard",
        description="Production-ready weather data service",
        version="0.0.1",
    )

    @app.get("/")
    async def root():
        return {"message": "Weather Analytics Dashboard API"}

    return app