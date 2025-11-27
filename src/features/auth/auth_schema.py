from __future__ import annotations

from pydantic import BaseModel, Field

from src.features.auth.auth_constants import AUTH_DEMO_PASSWORD, AUTH_DEMO_USERNAME


class AuthRegisterRequest(BaseModel):
    username: str = Field(default=AUTH_DEMO_USERNAME)
    password: str = Field(default=AUTH_DEMO_PASSWORD)


class AuthRegisterResponse(BaseModel):
    username: str


class AuthLoginRequest(BaseModel):
    username: str = Field(default=AUTH_DEMO_USERNAME)
    password: str = Field(default=AUTH_DEMO_PASSWORD)


class AuthLoginResponse(BaseModel):
    token: str

