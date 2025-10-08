from typing import Tuple, Optional
from src.model.req.bottle_req import CreateBottleReq
from src.constant.message.auth_message import SUCCESS
from src.constant.message.global_message import INTERNAL_ERROR
from src.repository.BottleRepository import BottleRepository


class BottleService:
    def __init__(self, repo: BottleRepository):
        self.repo = repo

    def create_bottle(
        self, payload: CreateBottleReq, sender_username: str
    ) -> Tuple[str, Optional[dict]]:
        try:
            bottle = self.repo.create_bottle(
                sender_username=sender_username,
                message=payload.message,
            )
            return SUCCESS, {
                "id": bottle.id,
                "sender_username": bottle.sender_username,
                "message": bottle.message,
            }
        except Exception:
            return INTERNAL_ERROR, None
