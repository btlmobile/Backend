from __future__ import annotations

from src.shared.base.singleton import Singleton
from src.shared.config.jwt import JwtManager


class TokenHelper(Singleton):
    def __init__(self) -> None:
        self._jwt_manager = JwtManager()

    def sign_username(self, username: str) -> str:
        return self._jwt_manager.sign({"sub": username})

    def verify(self, token: str) -> dict:
        return self._jwt_manager.verify(token)