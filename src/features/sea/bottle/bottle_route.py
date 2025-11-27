from fastapi import APIRouter, Header, Response, status

from src.features.sea.bottle.bottle_schema import BottleCreateSchema, BottleResponseSchema
from src.features.sea.bottle.bottle_service import BottleService


def create_router() -> APIRouter:
    router = APIRouter(prefix="/sea/bottle", tags=["sea-bottle"])
    service = BottleService()

    @router.post("", status_code=status.HTTP_204_NO_CONTENT)
    def create_bottle(payload: BottleCreateSchema, authorization: str | None = Header(default=None)) -> Response:
        service.create_bottle(payload, authorization)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.get("", response_model=BottleResponseSchema, status_code=status.HTTP_200_OK)
    def get_public_bottle() -> BottleResponseSchema:
        bottle = service.get_random_bottle()
        return BottleResponseSchema(**bottle)

    return router

