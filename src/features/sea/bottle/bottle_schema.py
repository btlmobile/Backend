from pydantic import BaseModel, Field


class BottleCreateSchema(BaseModel):
    type: str = Field(
        description="Loại bottle (ví dụ: text, html, markdown)",
        examples=["text"],
    )
    content: str = Field(
        description="Nội dung của bottle",
        examples=["Hello from the sea!"],
    )

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

