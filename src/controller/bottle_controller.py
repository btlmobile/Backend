from fastapi import APIRouter, Depends, status, Response, Request
from datetime import datetime, UTC
from sqlalchemy.orm import Session
from src.helper.db_session import get_db
from src.repository.BottleRepository import BottleRepository
from src.service.bottle_service import BottleService
from src.model.res.result_res import ResultRes
from src.model.req.bottle_req import CreateBottleReq
from src.constant.message.auth_message import SUCCESS, VALIDATION_ERROR
from src.helper.auth_helper import get_current_username

router = APIRouter()


def get_bottle_service(db: Session = Depends(get_db)):
    repo = BottleRepository(db)
    return BottleService(repo)


@router.post("/bottle", response_model=ResultRes, status_code=status.HTTP_201_CREATED)
def create_bottle(
    payload: CreateBottleReq,
    request: Request,
    response: Response,
    service: BottleService = Depends(get_bottle_service),
):
    username = get_current_username(request)
    if not username:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return ResultRes(
            isSuccess=False,
            errorCode="invalid_token",
            result=None,
            timeStamp=datetime.now(UTC).isoformat(),
        )

    message, result = service.create_bottle(payload, username)
    if message == SUCCESS:
        response.status_code = status.HTTP_201_CREATED
    elif message == VALIDATION_ERROR:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return ResultRes(
        isSuccess=message == SUCCESS,
        errorCode=message,
        result=result,
        timeStamp=datetime.now(UTC).isoformat(),
    )
