from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


ROLE_LEVEL = {
    Role.ADMIN: 1,
    Role.USER: 0,
}


def get_role_level(role: str) -> int:
    try:
        r = Role(role)
    except Exception:
        r = Role.USER
    return ROLE_LEVEL[r]

