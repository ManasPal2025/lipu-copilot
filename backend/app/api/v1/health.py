"""Health check endpoints for platform probes."""

from datetime import UTC, datetime
from typing import Literal

from fastapi import APIRouter, status
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
async def readiness() -> HealthResponse:
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

    overall: ServiceStatus = "ok" if all(value == "ok" for value in dependencies.values()) else "degraded"
    return HealthResponse(
        status=overall,
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        timestamp=datetime.now(UTC),
        dependencies=dependencies,
    )

