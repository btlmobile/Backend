from datetime import datetime
from pydantic import BaseModel, Field


class ChatCreateRequest(BaseModel):
    content: str = Field(
        description="Nội dung tin nhắn",
        examples=["Hello everyone!"],
        min_length=1,
        max_length=1000,
    )


class ChatResponse(BaseModel):
    id: str = Field(description="ID của tin nhắn")
    content: str = Field(description="Nội dung tin nhắn")
    sender: str = Field(description="Username người gửi")
    created_at: float = Field(description="Timestamp gửi tin (Unix timestamp)")
    is_me: bool = Field(description="Cờ đánh dấu tin nhắn của chính mình", default=False)
