from fastapi import APIRouter, Depends

from src.features.api.api_service import get_current_user


def create_router() -> APIRouter:
    router = APIRouter(prefix="/api", tags=["api"])

    @router.get(
        "/me",
        summary="Lấy thông tin user hiện tại",
        description="Lấy thông tin của user đang đăng nhập từ JWT token.",
        responses={
            200: {"description": "Thông tin user"},
            401: {"description": "Token không hợp lệ hoặc thiếu"},
        },
    )
    def get_current_user_info(current_user: str = Depends(get_current_user)) -> dict[str, str]:
        return {"username": current_user}

    return router

