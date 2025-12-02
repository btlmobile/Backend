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
        summary="Đăng ký tài khoản mới",
        description="Tạo tài khoản mới với username và password. Username và password phải từ 6-12 ký tự, không có ký tự đặc biệt.",
        responses={
            204: {"description": "Đăng ký thành công"},
            400: {"description": "Dữ liệu không hợp lệ"},
            409: {"description": "Username đã tồn tại"},
        },
    )
    def register_user(payload: AuthRegisterRequest) -> Response:
        user, error = auth_service.register(payload)
        if error:
            auth_service.raise_auth_error(error)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.post(
        "/login",
        response_model=AuthLoginResponse,
        summary="Đăng nhập",
        description="Đăng nhập với username và password. Trả về JWT token để sử dụng cho các request tiếp theo.",
        responses={
            200: {"description": "Đăng nhập thành công, trả về JWT token"},
            400: {"description": "Dữ liệu không hợp lệ"},
            401: {"description": "Sai username hoặc password"},
        },
    )
    def login_user(payload: AuthLoginRequest) -> AuthLoginResponse:
        result, error = auth_service.login(payload)
        if error:
            auth_service.raise_auth_error(error)
        return AuthLoginResponse(**result)

    return router

