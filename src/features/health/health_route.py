from fastapi import APIRouter

from src.features.health.health_service import build_health_payload


def create_router() -> APIRouter:
    router = APIRouter(prefix="/health", tags=["health"])
    router.add_api_route("", build_health_payload, methods=["GET"])
    return router

