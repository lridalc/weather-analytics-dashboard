"""Health check endpoint routes."""

from fastapi import APIRouter, status

from ..schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=HealthResponse,
    summary="Health check",
    description="Returns the health status of the service.",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse: Service health status."""
    return HealthResponse(status="healthy")
