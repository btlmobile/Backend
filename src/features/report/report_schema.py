from pydantic import BaseModel, Field

class ReportCreateRequest(BaseModel):
    bottle_id: str = Field(description="ID của bottle bị report")
    reason: str = Field(description="Lý do báo cáo", min_length=5, max_length=500)
