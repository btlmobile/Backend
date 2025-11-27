from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import jwt

from src.shared.constants.auth import AUTH_DEFAULT_SECRET, AUTH_JWT_ALG


class JwtManager:
    def __init__(
        self,
        secret_key: str | None = None,
        algorithm: str = AUTH_JWT_ALG,
        default_exp_minutes: int = 60,
    ) -> None:
        self._secret_key = secret_key or os.getenv("AUTH_JWT_SECRET", AUTH_DEFAULT_SECRET)
        self._algorithm = algorithm
        self._default_exp_minutes = default_exp_minutes

    def sign(self, payload: dict, expires_in_minutes: int | None = None) -> str:
        exp_minutes = expires_in_minutes or self._default_exp_minutes
        now = datetime.now(tz=timezone.utc)
        payload_with_exp = payload | {"exp": now + timedelta(minutes=exp_minutes)}
        token = jwt.encode(payload_with_exp, self._secret_key, algorithm=self._algorithm)
        return token

    def verify(self, token: str) -> dict:
        try:
            return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        except jwt.PyJWTError as exc:
            raise ValueError("invalid_token") from exc

