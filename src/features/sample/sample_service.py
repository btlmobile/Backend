from __future__ import annotations

from redis_om.model.model import NotFoundError

from src.features.sample.sample_message import (
    SAMPLE_EMPTY_UPDATE_ERROR,
    SAMPLE_NOT_FOUND_ERROR,
)
from src.features.sample.sample_entity import SampleEntity
from src.features.sample.sample_schema import SampleCreateSchema, SampleUpdateSchema
from src.shared.base.singleton import Singleton


class SampleService(Singleton):
    def create_sample(self, payload: SampleCreateSchema) -> tuple[SampleEntity | None, str | None]:
        sample = SampleEntity(**payload.model_dump())
        sample.save()
        return sample, None

    def list_samples(self) -> tuple[list[SampleEntity], str | None]:
        sample_ids = SampleEntity.all_pks()
        samples = [SampleEntity.get(sample_id) for sample_id in sample_ids]
        return samples, None

    def get_sample(self, sample_id: str) -> tuple[SampleEntity | None, str | None]:
        try:
            sample = SampleEntity.get(sample_id)
        except (KeyError, NotFoundError):
            return None, SAMPLE_NOT_FOUND_ERROR
        return sample, None

    def update_sample(self, sample_id: str, payload: SampleUpdateSchema) -> tuple[SampleEntity | None, str | None]:
        sample, error = self.get_sample(sample_id)
        if error:
            return None, error
        updates = payload.model_dump(exclude_unset=True, exclude_none=True)
        if not updates:
            return None, SAMPLE_EMPTY_UPDATE_ERROR
        for field, value in updates.items():
            setattr(sample, field, value)
        sample.save()
        return sample, None

    def delete_sample(self, sample_id: str) -> tuple[bool, str | None]:
        sample, error = self.get_sample(sample_id)
        if error:
            return False, error
        SampleEntity.delete(sample.pk)
        return True, None
