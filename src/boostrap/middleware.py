from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from redis_om.model.model import NotFoundError
from starlette.middleware.base import BaseHTTPMiddleware

from src.shared.constants.error_message import (
    ERROR_INTERNAL_SERVER,
    ERROR_RESOURCE_NOT_FOUND,
)
from src.shared.helpers.tokens import TokenHelper


from fastapi.middleware.cors import CORSMiddleware


def register_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ExceptionHandlerMiddleware)
    app.add_middleware(ApiAuthMiddleware)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(HTTPException, handle_http_exception)


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
                return _build_json_response(status.HTTP_401_UNAUTHORIZED, "auth_missing_token")
            token = auth_header.split(" ", 1)[1]
            try:
                self._token_helper.verify(token)
            except ValueError as exc:
                return _build_json_response(status.HTTP_401_UNAUTHORIZED, str(exc))
        return await call_next(request)


def _build_json_response(status_code: int, error_code: str) -> JSONResponse:
    payload = {"error_msg": error_code}
    return JSONResponse(content=payload, status_code=status_code)


async def handle_validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
    payload = {"error_msg": "invalid_payload"}
    return JSONResponse(content=payload, status_code=status.HTTP_400_BAD_REQUEST)


async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    error_msg = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    payload = {"error_msg": error_msg}
    return JSONResponse(content=payload, status_code=exc.status_code)

