"""Request context middleware for request IDs and access logs."""

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import Settings
from app.core.logging import get_logger


logger = get_logger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Attach request metadata and emit one structured access log per request."""

    def __init__(self, app: Callable[..., Awaitable[Response]], settings: Settings) -> None:
        super().__init__(app)
        self.settings = settings

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = request.headers.get(self.settings.request_id_header, str(uuid.uuid4()))
        request.state.request_id = request_id
        started = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((time.perf_counter() - started) * 1000, 2)
            logger.exception(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                },
            )
            raise

        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        response.headers[self.settings.request_id_header] = request_id
        response.headers["X-Process-Time-Ms"] = str(duration_ms)
        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        return response

