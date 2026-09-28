"""Health check endpoints for platform probes."""

from datetime import UTC, datetime
from typing import Literal

from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from app.core.config import get_settings
from app.db.redis import check_redis_connection
from app.db.session import check_database_connection


router = APIRouter(prefix="/health", tags=["health"])


ServiceStatus = Literal["ok", "degraded"]


class HealthResponse(BaseModel):
    status: ServiceStatus
    service: str
    version: str
    environment: str
    timestamp: datetime
    dependencies: dict[str, ServiceStatus] = {}


@router.get("/live", response_model=HealthResponse)
async def liveness() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        timestamp=datetime.now(UTC),
    )


@router.get("/ready", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def readiness(response: Response) -> HealthResponse:
    """Report whether required traffic dependencies are available.

    PostgreSQL is required. Redis is reported for visibility and does not
    change readiness, because no current request path uses it.
    """

    settings = get_settings()
    dependencies: dict[str, ServiceStatus] = {}

    try:
        await check_database_connection()
        dependencies["postgres"] = "ok"
    except Exception:
        dependencies["postgres"] = "degraded"

    try:
        await check_redis_connection()
        dependencies["redis"] = "ok"
    except Exception:
        dependencies["redis"] = "degraded"

    ready = dependencies["postgres"] == "ok"
    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return HealthResponse(
        status="ok" if ready else "degraded",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        timestamp=datetime.now(UTC),
        dependencies=dependencies,
    )

