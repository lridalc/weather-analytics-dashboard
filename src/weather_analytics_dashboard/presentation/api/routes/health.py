"""Health check endpoint routes."""

import logging

from fastapi import APIRouter, status

from ..schemas import HealthResponse

logger = logging.getLogger(__name__)
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
    # Observability log (DEBUG level because it is a very frequent endpoint)
    logger.debug("Health check requested")

    response: HealthResponse = HealthResponse(status="healthy")

    # Response log
    logger.debug(f"Health check completed with status: {response.status}")

    return response
