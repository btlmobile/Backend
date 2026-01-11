from datetime import datetime

from redis_om import Field, HashModel

from src.shared.base.redis_model import BaseRedisModel


class ChatEntity(BaseRedisModel, HashModel):
    content: str
    sender: str = Field(index=True)
    created_at: float = Field(index=True, sortable=True)

    class Meta(BaseRedisModel.Meta):
        model_key_prefix = "chat_global"
        ttl = 60 * 60 * 24 * 30  # Keep chat for 30 days
