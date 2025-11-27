from __future__ import annotations

from pydantic import BaseModel

from src.features.sample.sample_entity import SampleEntity


class SampleCreateSchema(BaseModel):
    name: str
    greeting: str


class SampleUpdateSchema(BaseModel):
    name: str | None = None
    greeting: str | None = None


class SampleResponseSchema(BaseModel):
    id: str
    name: str
    greeting: str


def build_sample_response(sample: SampleEntity) -> SampleResponseSchema:
    return SampleResponseSchema(
        id=sample.pk,
        name=sample.name,
        greeting=sample.greeting,
    )

