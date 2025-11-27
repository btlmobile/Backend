from __future__ import annotations

import os

from redis import Redis
from redis_om import get_redis_connection

from src.shared.base.singleton import Singleton
from src.shared.constants.redis import REDIS_DEFAULT_URL


class RedisClient(Singleton):
    def __init__(self) -> None:
        self._connection = self._build_connection()

    def get_connection(self) -> Redis:
        return self._connection

    def _build_connection(self) -> Redis:
        redis_url = os.getenv("REDIS_URL", REDIS_DEFAULT_URL)
        return get_redis_connection(url=redis_url, decode_responses=True)


