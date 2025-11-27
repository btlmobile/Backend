from fastapi import APIRouter, Response, status

from src.features.auth.auth_schema import (
    AuthLoginRequest,
    AuthLoginResponse,
    AuthRegisterRequest,
    AuthRegisterResponse,
)
from src.features.auth.auth_service import AuthService

auth_service = AuthService()


def create_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    @router.post(
        "/register",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def register_user(payload: AuthRegisterRequest) -> Response:
        user, error = auth_service.register(payload)
        if error:
            auth_service.raise_auth_error(error)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.post("/login", response_model=AuthLoginResponse)
    def login_user(payload: AuthLoginRequest) -> AuthLoginResponse:
        result, error = auth_service.login(payload)
        if error:
            auth_service.raise_auth_error(error)
        return AuthLoginResponse(**result)

    return router

