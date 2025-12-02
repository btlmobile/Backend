from __future__ import annotations

from pydantic import BaseModel, Field

from src.features.auth.auth_constants import AUTH_DEMO_PASSWORD, AUTH_DEMO_USERNAME


class AuthRegisterRequest(BaseModel):
    username: str = Field(
        default=AUTH_DEMO_USERNAME,
        description="Tên đăng nhập (6-12 ký tự, không có ký tự đặc biệt)",
        examples=["user123"],
        min_length=6,
        max_length=12,
    )
    password: str = Field(
        default=AUTH_DEMO_PASSWORD,
        description="Mật khẩu (6-12 ký tự, không có ký tự đặc biệt)",
        examples=["pass123"],
        min_length=6,
        max_length=12,
    )

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user123",
                "password": "pass123",
            }
        }


class AuthRegisterResponse(BaseModel):
    username: str = Field(description="Tên đăng nhập đã đăng ký")


class AuthLoginRequest(BaseModel):
    username: str = Field(
        default=AUTH_DEMO_USERNAME,
        description="Tên đăng nhập",
        examples=["user123"],
    )
    password: str = Field(
        default=AUTH_DEMO_PASSWORD,
        description="Mật khẩu",
        examples=["pass123"],
    )

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user123",
                "password": "pass123",
            }
        }


class AuthLoginResponse(BaseModel):
    token: str = Field(description="JWT token để xác thực các request tiếp theo")

