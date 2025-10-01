from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime, UTC


class ResultRes(BaseModel):
    isSuccess: bool
    errorCode: str
    result: Optional[Any] = None
    timeStamp: str = datetime.now(UTC).isoformat()
