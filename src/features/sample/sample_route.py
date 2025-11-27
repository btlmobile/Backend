from fastapi import APIRouter, status

from src.features.sample.sample_message import SAMPLE_ERROR_STATUS
from src.features.sample.sample_schema import (
    SampleCreateSchema,
    SampleResponseSchema,
    SampleUpdateSchema,
    build_sample_response,
)
from src.features.sample.sample_service import SampleService
from src.shared.utils.http_error import raise_http_error

sample_service = SampleService()

def create_router() -> APIRouter:
    router = APIRouter(prefix="/sample", tags=["sample"])

    @router.post("/", response_model=SampleResponseSchema)
    def create_sample(payload: SampleCreateSchema) -> SampleResponseSchema:
        sample, error = sample_service.create_sample(payload)
        if error:
            raise_http_error(error, SAMPLE_ERROR_STATUS)
        return build_sample_response(sample)

    @router.get("/", response_model=list[SampleResponseSchema])
    def list_samples() -> list[SampleResponseSchema]:
        samples, error = sample_service.list_samples()
        if error:
            raise_http_error(error, SAMPLE_ERROR_STATUS)
        return [build_sample_response(sample) for sample in samples]

    @router.get("/{sample_id}", response_model=SampleResponseSchema)
    def get_sample(sample_id: str) -> SampleResponseSchema:
        sample, error = sample_service.get_sample(sample_id)
        if error:
            raise_http_error(error, SAMPLE_ERROR_STATUS)
        return build_sample_response(sample)

    @router.put("/{sample_id}", response_model=SampleResponseSchema)
    def update_sample(sample_id: str, payload: SampleUpdateSchema) -> SampleResponseSchema:
        sample, error = sample_service.update_sample(sample_id, payload)
        if error:
            raise_http_error(error, SAMPLE_ERROR_STATUS)
        return build_sample_response(sample)

    @router.delete("/{sample_id}")
    def delete_sample(sample_id: str) -> dict[str, bool]:
        deleted, error = sample_service.delete_sample(sample_id)
        if error:
            raise_http_error(error, SAMPLE_ERROR_STATUS)
        return {"deleted": deleted}

    return router

