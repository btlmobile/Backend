from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from redis_om.model.model import NotFoundError
from starlette.middleware.base import BaseHTTPMiddleware

from src.shared.constants.error_message import (
    ERROR_INTERNAL_SERVER,
    ERROR_RESOURCE_NOT_FOUND,
)
from src.shared.helpers.tokens import TokenHelper


def register_middlewares(app: FastAPI) -> None:
    app.add_middleware(ExceptionHandlerMiddleware)
    app.add_middleware(ApiAuthMiddleware)
    app.add_exception_handler(RequestValidationError, handle_validation_error)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except NotFoundError:
            return _build_json_response(status.HTTP_404_NOT_FOUND, ERROR_RESOURCE_NOT_FOUND)
        except Exception:
            return _build_json_response(status.HTTP_500_INTERNAL_SERVER_ERROR, ERROR_INTERNAL_SERVER)


class ApiAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)
        self._token_helper = TokenHelper()

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    {"error": "auth_missing_token"},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            token = auth_header.split(" ", 1)[1]
            try:
                self._token_helper.verify(token)
            except ValueError as exc:
                return JSONResponse(
                    {"error": str(exc)},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
        return await call_next(request)


def _build_json_response(status_code: int, error_code: str) -> JSONResponse:
    payload = {"error": error_code}
    return JSONResponse(content=payload, status_code=status_code)


async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    payload = {"error": "invalid_payload", "message": "Payload không hợp lệ"}
    return JSONResponse(content=payload, status_code=status.HTTP_400_BAD_REQUEST)

