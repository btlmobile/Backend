from pydantic import BaseModel, Field, field_validator
import re


# Safe pattern - only alphanumeric, spaces, and basic punctuation
SAFE_TYPE_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{1,20}$")
MAX_CONTENT_LENGTH = 2000


class BottleCreateSchema(BaseModel):
    type: str = Field(
        description="Loại bottle (ví dụ: text, html, markdown)",
        examples=["text"],
        min_length=1,
        max_length=20,
    )
    content: str = Field(
        description="Nội dung của bottle",
        examples=["Hello from the sea!"],
        min_length=1,
        max_length=MAX_CONTENT_LENGTH,
    )

    @field_validator("type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        if not SAFE_TYPE_PATTERN.match(v):
            raise ValueError("Type must be alphanumeric, underscore, or hyphen only (1-20 chars)")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        # Block Redis protocol commands that could be injected
        dangerous_patterns = [
            r"^\*\d+",  # Redis protocol array
            r"^\$\d+",  # Redis protocol bulk string
            r"(?i)^(GET|SET|DEL|EVAL|SCRIPT|CONFIG|FLUSHALL|FLUSHDB|DEBUG|SHUTDOWN|SLAVEOF|REPLICAOF|AUTH|SAVE|BGSAVE)\s",
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, v):
                raise ValueError("Content contains invalid characters")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "type": "text",
                "content": "Hello from the sea!",
            }
        }


class BottleResponseSchema(BaseModel):
    id: str = Field(description="ID của bottle")
    type: str = Field(description="Loại bottle")
    content: str = Field(description="Nội dung của bottle")
    creator: str = Field(description="Username của người tạo (rỗng nếu ẩn danh)")

