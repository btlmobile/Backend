from pydantic import BaseModel


class BottleCreateSchema(BaseModel):
    type: str
    content: str


class BottleResponseSchema(BaseModel):
    id: str
    type: str
    content: str
    creator: str


class StoredBottleCreateSchema(BaseModel):
    bottle_id: str


class StoredBottleResponseSchema(BaseModel):
    id: str
    bottle_id: str
    bottle: BottleResponseSchema

