from typing import Tuple, Optional
from passlib.context import CryptContext
from src.model.req.auth_req import RegisterReq, LoginReq
from src.constant.message.auth_message import (
    SUCCESS,
    USER_EXISTS,
    INVALID_CREDENTIALS,
    VALIDATION_ERROR,
)
from src.repository.UserRepository import UserRepository
from src.helper.jwt_helper import create_access_token
from src.constant.role import Role

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def _hash_password(self, password: str) -> str:
        if len(password.encode("utf-8")) > 72:
            raise ValueError("password_too_long")
        try:
            return pwd_context.hash(password)
        except Exception:
            fallback = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
            return fallback.hash(password)

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def register(self, payload: RegisterReq) -> Tuple[str, Optional[dict]]:
        if self.repo.get_by_username(payload.username) is not None:
            return USER_EXISTS, None
        if self.repo.get_by_email(str(payload.email)) is not None:
            return USER_EXISTS, None
        try:
            hashed = self._hash_password(payload.password)
        except ValueError:
            return VALIDATION_ERROR, None
        user = self.repo.create_user(
            username=payload.username,
            email=str(payload.email),
            full_name=(payload.full_name or None),
            hashed_password=hashed,
            role=Role.USER,
        )
        extra_claims = {
            "username": user.username,
            "pwd_hash": user.hashed_password,
            "role": getattr(user, "role", "user"),
            "role_level": getattr(user, "role_level", 10),
        }
        access_token = create_access_token(
            subject=user.username, extra_claims=extra_claims
        )
        return SUCCESS, {
            "access_token": access_token,
            "token_type": "bearer",
        }

    def login(self, payload: LoginReq) -> Tuple[str, Optional[dict]]:
        user = self.repo.get_by_username(payload.username)
        if not user:
            return INVALID_CREDENTIALS, None
        try:
            if len(payload.password.encode("utf-8")) > 72:
                return VALIDATION_ERROR, None
        except Exception:
            return INVALID_CREDENTIALS, None
        if not self._verify_password(payload.password, user.hashed_password):
            return INVALID_CREDENTIALS, None
        extra_claims = {
            "username": user.username,
            "pwd_hash": user.hashed_password,
            "role": getattr(user, "role", "user"),
            "role_level": getattr(user, "role_level", 10),
        }
        access_token = create_access_token(
            subject=payload.username, extra_claims=extra_claims
        )
        return SUCCESS, {
            "access_token": access_token,
            "token_type": "bearer",
        }
