"""Health check endpoint schemas."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "healthy",
            }
        }
    }

    status: str = Field(
        default="healthy",
        description="Current health status of the service.",
        examples=["healthy"],
        pattern="^(healthy|degraded|unhealthy)$",
    )
