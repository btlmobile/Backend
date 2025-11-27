from __future__ import annotations

from redis_om.model.model import NotFoundError

from src.features.auth.auth_entity import AuthUserEntity
from src.features.auth.auth_helper import validate_password, validate_username
from src.features.auth.auth_message import (
    AUTH_ERROR_STATUS,
    AUTH_INTERNAL_ERROR,
    AUTH_PASSWORD_INVALID,
    AUTH_UNAUTHORIZED,
    AUTH_USER_EXISTS_ERROR,
    AUTH_USERNAME_INVALID,
)
from src.features.auth.auth_schema import AuthLoginRequest, AuthRegisterRequest
from src.shared.helpers.tokens import TokenHelper
from src.shared.base.singleton import Singleton
from src.shared.utils.http_error import raise_http_error


class AuthService(Singleton):
    def __init__(self) -> None:
        self._token_helper = TokenHelper()

    def register(self, payload: AuthRegisterRequest) -> tuple[AuthUserEntity | None, str | None]:
        validation_error = self._validate_credentials(payload)
        if validation_error:
            return None, validation_error
        existing_user = self._find_user(payload.username)
        if existing_user:
            return None, AUTH_USER_EXISTS_ERROR
        try:
            user = AuthUserEntity(username=payload.username, password=payload.password)
            user.save()
            return user, None
        except Exception:
            return None, AUTH_INTERNAL_ERROR

    def login(self, payload: AuthLoginRequest) -> tuple[dict | None, str | None]:
        validation_error = self._validate_credentials(payload)
        if validation_error:
            return None, validation_error
        user = self._find_user(payload.username)
        if not user or user.password != payload.password:
            return None, AUTH_UNAUTHORIZED
        token = self._token_helper.sign_username(user.username)
        return {"token": token}, None

    def raise_auth_error(self, error_code: str) -> None:
        raise_http_error(error_code, AUTH_ERROR_STATUS, AUTH_ERROR_STATUS[AUTH_INTERNAL_ERROR])

    def _find_user(self, username: str) -> AuthUserEntity | None:
        try:
            return AuthUserEntity.find(AuthUserEntity.username == username).first()
        except NotFoundError:
            return None

    def _validate_credentials(self, payload: AuthRegisterRequest) -> str | None:
        try:
            validate_username(payload.username)
        except ValueError:
            return AUTH_USERNAME_INVALID
            
        try:
            validate_password(payload.password)
        except ValueError:
            return AUTH_PASSWORD_INVALID
        return None

