"""Application exception types and handlers."""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import get_logger


logger = get_logger(__name__)


class AppError(Exception):
    """Base application error with a stable client-facing code."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "internal_error"
    message: str = "An unexpected error occurred."

    def __init__(
        self,
        message: str | None = None,
        *,
        status_code: int | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.message
        self.status_code = status_code or self.status_code
        self.code = code or self.code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"
    message = "The requested resource was not found."


class BadRequestError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "bad_request"
    message = "The request is invalid."


class ConflictError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"
    message = "The request conflicts with the current resource state."


class ExternalServiceError(AppError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "external_service_unavailable"
    message = "An upstream service is unavailable."


def error_payload(request: Request, code: str, message: str, details: Any | None = None) -> dict[str, Any]:
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details,
            "request_id": getattr(request.state, "request_id", None),
        }
    }


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    logger.warning(
        "Application error",
        extra={"request_id": getattr(request.state, "request_id", None), "path": request.url.path, "code": exc.code},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(request, exc.code, exc.message, exc.details),
    )


async def http_error_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(request, "http_error", str(exc.detail)),
        headers=getattr(exc, "headers", None),
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_payload(request, "validation_error", "Request validation failed.", exc.errors()),
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled application error",
        extra={"request_id": getattr(request.state, "request_id", None), "path": request.url.path},
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_payload(request, "internal_error", "An unexpected error occurred."),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
