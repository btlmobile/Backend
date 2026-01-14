from redis_om import Field

from src.shared.base.redis_model import BaseRedisModel


class ChatEntity(BaseRedisModel):
    content: str
    sender: str = Field(index=True)
    created_at: float = Field(index=True, sortable=True)

    class Meta(BaseRedisModel.Meta):
        model_key_prefix = "chat_global"
        index_name = "app:src.features.chat.chat_entity.ChatEntity:index"

