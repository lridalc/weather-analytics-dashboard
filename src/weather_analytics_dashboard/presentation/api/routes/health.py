"""Health check endpoint routes."""

from fastapi import APIRouter, status

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Returns the health status of the service.",
)
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict: Simple status response indicating service health."""
    return {"status": "healthy"}
