from fastapi import APIRouter, Depends, Query, Response, status

from src.features.api.api_service import get_current_user
from src.features.api.bottle.bottle_schema import (
    BottleCreateSchema,
    BottleResponseSchema,
    StoredBottleCreateSchema,
    StoredBottleResponseSchema,
)
from src.features.api.bottle.bottle_service import BottleService


def _build_bottle_response(bottle) -> BottleResponseSchema:
    return BottleResponseSchema(
        id=bottle.pk,
        type=bottle.type,
        content=bottle.content,
        creator=bottle.creator,
    )


def create_router() -> APIRouter:
    router = APIRouter(prefix="/api/bottle", tags=["api-bottle"])
    service = BottleService()

    @router.post("", status_code=status.HTTP_204_NO_CONTENT)
    def create_bottle(
        payload: BottleCreateSchema,
        current_user: str = Depends(get_current_user),
    ) -> Response:
        bottle, error = service.create_bottle(payload, current_user)
        if error:
            service.raise_bottle_error(error)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.get("", response_model=list[BottleResponseSchema])
    def list_bottles(
        page: int = Query(default=1, ge=1),
        current_user: str = Depends(get_current_user),
    ) -> list[BottleResponseSchema]:
        bottles, error = service.list_bottles(page=page, limit=5)
        if error:
            service.raise_bottle_error(error)
        return [_build_bottle_response(bottle) for bottle in bottles]

    @router.delete("/{bottle_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_bottle(
        bottle_id: str,
        current_user: str = Depends(get_current_user),
    ) -> Response:
        deleted, error = service.delete_bottle(bottle_id)
        if error:
            service.raise_bottle_error(error)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.post("/store", status_code=status.HTTP_204_NO_CONTENT)
    def create_stored_bottle(
        payload: StoredBottleCreateSchema,
        current_user: str = Depends(get_current_user),
    ) -> Response:
        stored, error = service.create_stored_bottle(payload.bottle_id, current_user)
        if error:
            service.raise_bottle_error(error)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.get("/store", response_model=list[StoredBottleResponseSchema])
    def list_stored_bottles(
        page: int = Query(default=1, ge=1),
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

    @router.delete("/store/{stored_bottle_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_stored_bottle(
        stored_bottle_id: str,
        current_user: str = Depends(get_current_user),
    ) -> Response:
        deleted, error = service.delete_stored_bottle(stored_bottle_id, current_user)
        if error:
            service.raise_bottle_error(error)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return router

