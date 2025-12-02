from redis_om import Field, HashModel

from src.shared.base.redis_model import BaseRedisModel


class StoredBottleEntity(BaseRedisModel, HashModel):
    bottle_id: str = Field(index=True)
    user_id: str = Field(index=True)

    class Meta(BaseRedisModel.Meta):
        model_key_prefix = "stored_bottle"

