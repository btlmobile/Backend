from pydantic import BaseModel


class BottleCreateSchema(BaseModel):
    type: str
    content: str


class BottleResponseSchema(BaseModel):
    id: str
    type: str
    content: str
    creator: str

