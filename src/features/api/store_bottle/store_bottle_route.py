from fastapi import APIRouter, Depends, Query, Response, status

from src.features.api.api_service import get_current_user
from src.features.api.store_bottle.store_bottle_schema import (
    BottleResponseSchema,
    StoredBottleCreateSchema,
    StoredBottleResponseSchema,
)
from src.features.api.store_bottle.store_bottle_service import BottleService


def _build_bottle_response(bottle) -> BottleResponseSchema:
    return BottleResponseSchema(
        id=bottle.pk,
        type=bottle.type,
        content=bottle.content,
        creator=bottle.creator,
    )


def create_router() -> APIRouter:
    router = APIRouter(prefix="/api/store-bottle", tags=["api-store-bottle"])
    service = BottleService()

    @router.post(
        "",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Lưu bottle vào danh sách",
        description="Lưu một bottle vào danh sách stored bottles của user. Mỗi bottle chỉ có thể lưu một lần cho mỗi user.",
        responses={
            204: {"description": "Lưu bottle thành công"},
            404: {"description": "Bottle không tồn tại"},
            409: {"description": "Bottle đã được lưu trước đó"},
        },
    )
    def create_stored_bottle(
        payload: StoredBottleCreateSchema,
        current_user: str = Depends(get_current_user),
    ) -> Response:
        stored, error = service.create_stored_bottle(payload.bottle_id, current_user)
        if error:
            service.raise_bottle_error(error)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.get(
        "",
        response_model=list[StoredBottleResponseSchema],
        summary="Lấy danh sách stored bottles",
        description="Lấy danh sách các bottles đã lưu của user hiện tại. Hỗ trợ phân trang, mỗi trang 5 items.",
        responses={
            200: {"description": "Danh sách stored bottles"},
        },
    )
    def list_stored_bottles(
        page: int = Query(default=1, ge=1, description="Số trang (bắt đầu từ 1)"),
        current_user: str = Depends(get_current_user),
    ) -> list[StoredBottleResponseSchema]:
        stored_bottles, error = service.list_stored_bottles(current_user, page=page, limit=5)
        if error:
            service.raise_bottle_error(error)
        return [
            StoredBottleResponseSchema(
                id=stored.pk,
                bottle_id=stored.bottle_id,
                bottle=_build_bottle_response(bottle),
            )
            for stored, bottle in stored_bottles
        ]

    @router.get(
        "/{stored_bottle_id}",
        response_model=StoredBottleResponseSchema,
        summary="Lấy chi tiết stored bottle",
        description="Lấy thông tin chi tiết của một stored bottle theo ID. Chỉ có thể lấy stored bottle của chính user.",
        responses={
            200: {"description": "Thông tin stored bottle"},
            404: {"description": "Stored bottle không tồn tại hoặc không thuộc về user"},
        },
    )
    def get_stored_bottle(
        stored_bottle_id: str,
        current_user: str = Depends(get_current_user),
    ) -> StoredBottleResponseSchema:
        result, error = service.get_stored_bottle(stored_bottle_id, current_user)
        if error:
            service.raise_bottle_error(error)
        stored, bottle = result
        return StoredBottleResponseSchema(
            id=stored.pk,
            bottle_id=stored.bottle_id,
            bottle=_build_bottle_response(bottle),
        )

    @router.delete(
        "/{stored_bottle_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary="Xóa stored bottle",
        description="Xóa một stored bottle khỏi danh sách. Chỉ có thể xóa stored bottle của chính user. Bottle gốc không bị xóa.",
        responses={
            204: {"description": "Xóa thành công"},
            404: {"description": "Stored bottle không tồn tại hoặc không thuộc về user"},
        },
    )
    def delete_stored_bottle(
        stored_bottle_id: str,
        current_user: str = Depends(get_current_user),
    ) -> Response:
        deleted, error = service.delete_stored_bottle(stored_bottle_id, current_user)
        if error:
            service.raise_bottle_error(error)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router

