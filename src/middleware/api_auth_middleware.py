from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from datetime import datetime, UTC
from src.helper.jwt_helper import verify_token
from src.model.res.result_res import ResultRes


class ApiAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path
        if not path.startswith("/api/"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            res = ResultRes(
                isSuccess=False,
                errorCode="invalid_token",
                result=None,
                timeStamp=datetime.now(UTC).isoformat(),
            )
            return JSONResponse(status_code=401, content=res.model_dump())

        token = auth_header.split(" ", 1)[1]
        payload = verify_token(token)
        if not payload:
            res = ResultRes(
                isSuccess=False,
                errorCode="invalid_token",
                result=None,
                timeStamp=datetime.now(UTC).isoformat(),
            )
            return JSONResponse(status_code=401, content=res.model_dump())

        role_level = payload.get("role_level")

        if role_level is None or role_level < 0:
            res = ResultRes(
                isSuccess=False,
                errorCode="forbidden",
                result=None,
                timeStamp=datetime.now(UTC).isoformat(),
            )
            return JSONResponse(status_code=403, content=res.model_dump())

        return await call_next(request)
