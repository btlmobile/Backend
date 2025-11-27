from redis_om import Field, HashModel

from src.shared.base.redis_model import BaseRedisModel


class BottleEntity(BaseRedisModel, HashModel):
    type: str = Field(index=True)
    content: str
    creator: str = Field(index=True)

    class Meta(BaseRedisModel.Meta):
        model_key_prefix = "bottle"
        ttl = 60 * 60 * 24 * 7

