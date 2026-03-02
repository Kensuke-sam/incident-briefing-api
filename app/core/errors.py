from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class AppError(Exception):
    def __init__(self, status_code: int, code: str, message: str) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message


class AuthorizationError(AppError):
    def __init__(self, message: str = "Unauthorized request.") -> None:
        super().__init__(status_code=401, code="unauthorized", message=message)


class NotFoundError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(status_code=404, code="not_found", message=message)


class PersistenceError(AppError):
    def __init__(self, message: str = "Database operation failed.") -> None:
        super().__init__(status_code=500, code="persistence_error", message=message)


class ExternalServiceError(AppError):
    def __init__(self, message: str = "External service failed.") -> None:
        super().__init__(status_code=502, code="external_service_error", message=message)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {"code": exc.code, "message": exc.message},
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled application error", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_server_error",
                    "message": "Unexpected server error.",
                },
                "request_id": getattr(request.state, "request_id", "unknown"),
            },
        )
