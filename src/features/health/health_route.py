from fastapi import APIRouter

from src.features.health.health_service import build_health_payload


def create_router() -> APIRouter:
    router = APIRouter(prefix="/health", tags=["health"])
    router.add_api_route(
        "",
        build_health_payload,
        methods=["GET"],
        summary="Health check",
        description="Kiểm tra trạng thái sức khỏe của hệ thống. Endpoint công khai, không cần xác thực.",
        responses={
            200: {"description": "Hệ thống hoạt động bình thường"},
        },
    )
    return router

