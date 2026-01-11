from pydantic import BaseModel, Field, field_validator
import re


# ULID pattern - 26 characters, base32 (Crockford's)
ULID_PATTERN = re.compile(r"^[0-9A-HJKMNP-TV-Z]{26}$")


class BottleResponseSchema(BaseModel):
    id: str = Field(description="ID của bottle")
    type: str = Field(description="Loại bottle")
    content: str = Field(description="Nội dung của bottle")
    creator: str = Field(description="Username của người tạo")


class StoredBottleCreateSchema(BaseModel):
    bottle_id: str = Field(
        description="ID của bottle muốn lưu",
        examples=["01KB2GQ4HMSM6ZZKEH580PV91J"],
        min_length=26,
        max_length=26,
    )

    @field_validator("bottle_id")
    @classmethod
    def validate_bottle_id(cls, v: str) -> str:
        if not ULID_PATTERN.match(v):
            raise ValueError("bottle_id must be a valid ULID format")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "bottle_id": "01KB2GQ4HMSM6ZZKEH580PV91J",
            }
        }


class StoredBottleResponseSchema(BaseModel):
    id: str = Field(description="ID của stored bottle record")
    bottle_id: str = Field(description="ID của bottle đã lưu")
    bottle: BottleResponseSchema = Field(description="Thông tin chi tiết của bottle")

