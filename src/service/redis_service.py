from typing import Any

from src.helper.settings_helper import load_settings

try:
    from redis import Redis
    from redis_om import get_redis_connection
except Exception:
    Redis = None


class RedisService:
    _client: Any = None
    _config: dict = load_settings().get("redis", {})

    @classmethod
    def get_redis_client(cls) -> Any:
        if cls._client is None:
            host = cls._config.get("host") or "localhost"
            port = int(cls._config.get("port", 6379))
            password = cls._config.get("password")
            cls._client = Redis(host=host, port=port, password=password, decode_responses=True)
        return cls._client

    @classmethod
    def get_redis_om_connection(cls):
        host = cls._config.get("host") or "localhost"
        port = int(cls._config.get("port", 6379))
        password = cls._config.get("password")
        return get_redis_connection(host=host, port=port, password=password, decode_responses=True)
