from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class RegisterReq(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)
    full_name: Optional[str] = None

    @field_validator("password")
    def password_max_bytes(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password_too_long")
        return v


class LoginReq(BaseModel):
    username: str
    password: str = Field(min_length=6, max_length=72)

    @field_validator("password")
    def password_max_bytes(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("password_too_long")
        return v
