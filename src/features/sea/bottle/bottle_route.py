from fastapi import APIRouter, Header, Response, status

from src.features.sea.bottle.bottle_schema import BottleCreateSchema, BottleResponseSchema
from src.features.sea.bottle.bottle_service import BottleService


def create_router() -> APIRouter:
    router = APIRouter(prefix="/sea/bottle", tags=["sea-bottle"])
    service = BottleService()

    @router.post(
        "",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Tạo bottle mới",
        description="Tạo một bottle mới và thả vào biển. Có thể tạo ẩn danh (không có token) hoặc có creator (có token).",
        responses={
            204: {"description": "Tạo bottle thành công"},
            400: {"description": "Dữ liệu không hợp lệ"},
        },
    )
    def create_bottle(payload: BottleCreateSchema, authorization: str | None = Header(default=None)) -> Response:
        service.create_bottle(payload, authorization)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.get(
        "",
        response_model=BottleResponseSchema,
        status_code=status.HTTP_200_OK,
        summary="Lấy bottle ngẫu nhiên",
        description="Lấy một bottle ngẫu nhiên từ biển. Endpoint công khai, không cần xác thực.",
        responses={
            200: {"description": "Trả về bottle ngẫu nhiên"},
        },
    )
    def get_public_bottle() -> BottleResponseSchema:
        bottle = service.get_random_bottle()
        return BottleResponseSchema(**bottle)

    return router

