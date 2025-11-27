from __future__ import annotations

import random

from fastapi import Header
from redis_om import NotFoundError

from src.features.sea.bottle.bottle_entity import BottleEntity
from src.shared.base.singleton import Singleton
from src.shared.helpers.tokens import TokenHelper


class BottleService(Singleton):
    def __init__(self) -> None:
        self._token_helper = TokenHelper()

    def create_bottle(self, payload, authorization: str | None = None) -> None:
        creator = self._extract_user(authorization)
        bottle = BottleEntity(type=payload.type, content=payload.content, creator=creator)
        bottle.save()

    def get_random_bottle(self) -> dict[str, str]:
        try:
            all_ids = list(BottleEntity.all_pks())
            if not all_ids:
                return {"id": "", "type": "", "content": "", "creator": ""}
            random_id = random.choice(all_ids)
            bottle = BottleEntity.get(random_id)
            return {
                "id": bottle.pk,
                "type": bottle.type,
                "content": bottle.content,
                "creator": bottle.creator,
            }
        except (Exception, NotFoundError):
            return {"id": "", "type": "", "content": "", "creator": ""}

    def _extract_user(self, authorization: str | None) -> str:
        if not authorization or not authorization.startswith("Bearer "):
            return ""
        try:
            token = authorization.split(" ", 1)[1]
            claims = self._token_helper.verify(token)
            return claims.get("sub", "")
        except Exception:
            return ""

