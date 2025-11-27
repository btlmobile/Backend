from src.shared.base.redis_model import BaseRedisModel


class SampleEntity(BaseRedisModel):
    name: str
    greeting: str


