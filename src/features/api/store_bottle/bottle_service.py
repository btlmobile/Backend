from __future__ import annotations

from redis_om.model.model import NotFoundError

from src.features.api.store_bottle.bottle_message import (
    BOTTLE_ERROR_STATUS,
    BOTTLE_NOT_FOUND_ERROR,
    STORED_BOTTLE_ALREADY_EXISTS_ERROR,
    STORED_BOTTLE_NOT_FOUND_ERROR,
)
from src.features.api.store_bottle.stored_bottle_entity import StoredBottleEntity
from src.features.sea.bottle.bottle_entity import BottleEntity
from src.shared.base.singleton import Singleton
from src.shared.utils.http_error import raise_http_error


class BottleService(Singleton):
    def _get_bottle(self, bottle_id: str) -> tuple[BottleEntity | None, str | None]:
        try:
            bottle = BottleEntity.get(bottle_id)
            return bottle, None
        except NotFoundError:
            return None, BOTTLE_NOT_FOUND_ERROR

    def create_stored_bottle(self, bottle_id: str, user_id: str) -> tuple[StoredBottleEntity | None, str | None]:
        bottle, error = self._get_bottle(bottle_id)
        if error:
            return None, error
        existing = self._find_stored_bottle(bottle_id, user_id)
        if existing:
            return None, STORED_BOTTLE_ALREADY_EXISTS_ERROR
        try:
            stored = StoredBottleEntity(bottle_id=bottle_id, user_id=user_id)
            stored.save()
            return stored, None
        except Exception:
            return None, None

    def list_stored_bottles(self, user_id: str, page: int = 1, limit: int = 5) -> tuple[list[tuple[StoredBottleEntity, BottleEntity]], str | None]:
        try:
            stored_bottles = list(StoredBottleEntity.find(StoredBottleEntity.user_id == user_id).all())
            start = (page - 1) * limit
            end = start + limit
            page_stored = stored_bottles[start:end]
            result = []
            for stored in page_stored:
                try:
                    bottle = BottleEntity.get(stored.bottle_id)
                    result.append((stored, bottle))
                except NotFoundError:
                    continue
            return result, None
        except Exception:
            return [], None

    def delete_stored_bottle(self, stored_bottle_id: str, user_id: str) -> tuple[bool, str | None]:
        try:
            stored = StoredBottleEntity.get(stored_bottle_id)
            if stored.user_id != user_id:
                return False, STORED_BOTTLE_NOT_FOUND_ERROR
            StoredBottleEntity.delete(stored.pk)
            return True, None
        except NotFoundError:
            return False, STORED_BOTTLE_NOT_FOUND_ERROR

    def _find_stored_bottle(self, bottle_id: str, user_id: str) -> StoredBottleEntity | None:
        try:
            return StoredBottleEntity.find(
                StoredBottleEntity.bottle_id == bottle_id,
                StoredBottleEntity.user_id == user_id,
            ).first()
        except NotFoundError:
            return None

    def raise_bottle_error(self, error_code: str) -> None:
        raise_http_error(error_code, BOTTLE_ERROR_STATUS)

