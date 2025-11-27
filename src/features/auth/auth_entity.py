from redis_om import Field

from src.shared.base.redis_model import BaseRedisModel


class AuthUserEntity(BaseRedisModel):
    username: str = Field(index=True)
    password: str

