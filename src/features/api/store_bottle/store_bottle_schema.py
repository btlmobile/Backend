from pydantic import BaseModel, Field


class BottleResponseSchema(BaseModel):
    id: str = Field(description="ID của bottle")
    type: str = Field(description="Loại bottle")
    content: str = Field(description="Nội dung của bottle")
    creator: str = Field(description="Username của người tạo")


class StoredBottleCreateSchema(BaseModel):
    bottle_id: str = Field(
        description="ID của bottle muốn lưu",
        examples=["01KB2GQ4HMSM6ZZKEH580PV91J"],
    )

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

