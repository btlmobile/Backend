from __future__ import annotations

import time

from redis_om import NotFoundError

from src.features.chat.chat_entity import ChatEntity
from src.features.chat.chat_schema import ChatCreateRequest, ChatResponse
from src.shared.base.singleton import Singleton
from src.shared.helpers.tokens import TokenHelper


class ChatService(Singleton):
    def __init__(self) -> None:
        self._token_helper = TokenHelper()

    def create_message(self, payload: ChatCreateRequest, authorization: str) -> tuple[ChatEntity | None, str | None]:
        sender = self._extract_user(authorization)
        if not sender:
             # Should be handled by Auth middleware but just in case
            return None, "auth_required"
        
        try:
            chat = ChatEntity(
                content=payload.content,
                sender=sender,
                created_at=time.time()
            )
            chat.save()
            return chat, None
        except Exception:
            return None, "internal_error"

    def get_messages(self, limit: int = 50, authorization: str | None = None) -> list[dict]:
        # Fetch all (limited in scale by TTL and practical usage for now)
        # Using Python sort to ensure reliability if Redis syntax fails
        results = ChatEntity.find().all()
        results.sort(key=lambda x: x.created_at, reverse=True)
        results = results[:limit]
        
        current_user = self._extract_user(authorization) if authorization else ""
        
        response = []
        for chat in results:
            response.append({
                "id": chat.pk,
                "content": chat.content,
                "sender": chat.sender,
                "created_at": chat.created_at,
                "is_me": chat.sender == current_user
            })
        
        return response

    def _extract_user(self, authorization: str | None) -> str:
        if not authorization or not authorization.startswith("Bearer "):
            return ""
        try:
            token = authorization.split(" ", 1)[1]
            claims = self._token_helper.verify(token)
            return claims.get("sub", "")
        except Exception:
            return ""
