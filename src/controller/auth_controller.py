from fastapi import APIRouter, Depends, status, Response
from datetime import datetime, UTC

from sqlalchemy.orm import Session
from src.helper.db_session import get_db
from src.repository.UserRepository import UserRepository
from src.service.auth_service import AuthService
from src.model.res.result_res import ResultRes
from src.model.req.auth_req import RegisterReq, LoginReq
from src.constant.message.auth_message import SUCCESS, USER_EXISTS, INVALID_CREDENTIALS, VALIDATION_ERROR
from src.helper.jwt_helper import get_current_user

router = APIRouter()


def get_auth_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return AuthService(repo)


@router.post("/register", response_model=ResultRes, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterReq, response: Response, service: AuthService = Depends(get_auth_service)):
    message, result = service.register(payload)
    if message == SUCCESS:
        response.status_code = status.HTTP_201_CREATED
    elif message == VALIDATION_ERROR:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
    return ResultRes(
        isSuccess=message == SUCCESS,
        errorCode=message,
        result=result,
        timeStamp=datetime.now(UTC).isoformat(),
    )


@router.post("/login", response_model=ResultRes)
def login(payload: LoginReq, response: Response, service: AuthService = Depends(get_auth_service)):
    message, result = service.login(payload)
    if message == SUCCESS:
        response.status_code = status.HTTP_200_OK
    elif message == VALIDATION_ERROR:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
    return ResultRes(
        isSuccess=message == SUCCESS,
        errorCode=message,
        result=result,
        timeStamp=datetime.now(UTC).isoformat(),
    )


@router.get("/me", response_model=ResultRes)
def me(current_user=Depends(get_current_user)):
    return ResultRes(
        isSuccess=True,
        errorCode=SUCCESS,
        result={
            "username": current_user.username,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "is_active": current_user.is_active,
        },
        timeStamp=datetime.now(UTC).isoformat(),
    )
