from __future__ import annotations

from redis_om import HashModel

from src.shared.config.redis_client import RedisClient

REDIS_CONNECTION = RedisClient().get_connection()


class BaseRedisModel(HashModel):
    class Meta:
        database = REDIS_CONNECTION
        global_key_prefix = "app"

