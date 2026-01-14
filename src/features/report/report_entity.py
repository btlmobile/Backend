from redis_om import Field
from src.shared.base.redis_model import BaseRedisModel

class ReportEntity(BaseRedisModel):
    reporter: str = Field(index=True)
    bottle_id: str = Field(index=True)
    reason: str
    created_at: float = Field(index=True, sortable=True)

    class Meta(BaseRedisModel.Meta):
        model_key_prefix = "report"
        index_name = "app:src.features.report.report_entity.ReportEntity:index"
