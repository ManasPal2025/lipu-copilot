"""FastAPI application factory and runtime lifecycle."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.v1.router import api_router
from app.core.config import Settings, get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.db.redis import close_redis_connection
from app.db.session import close_database_connections
from app.middleware.request_context import RequestContextMiddleware
from app.middleware.security import SecurityHeadersMiddleware


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()
    logger.info("Starting application", extra={"service": settings.app_name, "version": settings.app_version})
    yield
    logger.info("Shutting down application")
    await close_redis_connection()
    await close_database_connections()


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the FastAPI application."""

    settings = settings or get_settings()
    configure_logging(settings)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
        lifespan=lifespan,
    )

    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestContextMiddleware, settings=settings)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)

    register_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/", tags=["system"])
    async def root() -> dict[str, str]:
        return {"service": settings.app_name, "version": settings.app_version, "status": "ok"}

    return app


app = create_app()

