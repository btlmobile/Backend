import logging
from datetime import datetime, UTC
from fastapi import HTTPException, Request, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import text


def init_routes(app: FastAPI) -> None:
    @app.get("/health", tags=["Health"])
    def health():
        return {"status": "ok"}

    @app.get("/health/mysql", tags=["Health"])
    def health_mysql():
        try:
            from src.config.db_dev import engine

            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return {"mysql": True}
        except Exception as e:
            logging.getLogger("app").error("mysql health check failed: %s", str(e))
            return {"mysql": False}

    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):
        from src.model.res.result_res import ResultRes

        return JSONResponse(
            status_code=exc.status_code,
            content=ResultRes(
                isSuccess=False,
                errorCode=str(exc.detail) if exc.detail else "http_error",
                result=None,
                timeStamp=datetime.now(UTC).isoformat(),
            ).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request: Request, exc: RequestValidationError):
        from src.model.res.result_res import ResultRes

        return JSONResponse(
            status_code=422,
            content=ResultRes(
                isSuccess=False,
                errorCode="validation_error",
                result={"errors": exc.errors()},
                timeStamp=datetime.now(UTC).isoformat(),
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    def unhandled_exception_handler(request: Request, exc: Exception):
        from src.model.res.result_res import ResultRes

        return JSONResponse(
            status_code=500,
            content=ResultRes(
                isSuccess=False,
                errorCode="internal_error",
                result=None,
                timeStamp=datetime.now(UTC).isoformat(),
            ).model_dump(),
        )
