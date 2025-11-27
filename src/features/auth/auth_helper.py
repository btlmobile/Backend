from __future__ import annotations

import re

from src.features.auth.auth_message import (
    AUTH_PASSWORD_INVALID,
    AUTH_USERNAME_INVALID,
)

USERNAME_PASSWORD_PATTERN = re.compile(r"^[A-Za-z0-9]{6,12}$")


def validate_username(value: str) -> str:
    if not USERNAME_PASSWORD_PATTERN.fullmatch(value):
        raise ValueError(AUTH_USERNAME_INVALID)
    return value


def validate_password(value: str) -> str:
    if not USERNAME_PASSWORD_PATTERN.fullmatch(value):
        raise ValueError(AUTH_PASSWORD_INVALID)
    return value
