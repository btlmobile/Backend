from fastapi import FastAPI
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime, UTC
from src.route.auth_route import router as auth_router
from src.helper.settings_helper import load_settings
from fastapi.openapi.utils import get_openapi
import logging
from sqlalchemy import text
from src.middleware.health_admin_middleware import HealthAdminMiddleware

settings = load_settings()
server_cfg = settings.get("server", {})

openapi_tags = [
    {"name": "Health", "description": "Health check endpoints"},
    {"name": "Auth", "description": "Authentication endpoints"},
]

app = FastAPI(title="BTL Mobile Backend", version="0.1.0", openapi_tags=openapi_tags)

app.add_middleware(HealthAdminMiddleware)
app.include_router(auth_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

try:
    from src.config.db_dev import Base, engine, database
    Base.metadata.create_all(bind=engine)
    from sqlalchemy import text
    with engine.connect() as conn:
        check_role = conn.execute(text(
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=:db AND TABLE_NAME='users' AND COLUMN_NAME='role'"
        ), {"db": database}).scalar_one()
        if int(check_role) == 0:
            conn.execute(text("ALTER TABLE users ADD COLUMN `role` VARCHAR(32) NOT NULL DEFAULT 'user'"))
        check_role_level = conn.execute(text(
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA=:db AND TABLE_NAME='users' AND COLUMN_NAME='role_level'"
        ), {"db": database}).scalar_one()
        if int(check_role_level) == 0:
            conn.execute(text("ALTER TABLE users ADD COLUMN `role_level` INT NOT NULL DEFAULT 0"))
        conn.commit()
except Exception as e:
    logging.getLogger("app").error("startup failed: %s", str(e))


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


if __name__ == "__main__":
    import uvicorn

    host = server_cfg.get("host", "127.0.0.1")
    port = int(server_cfg.get("port", 8000))
    reload = bool(server_cfg.get("reload", False))
    uvicorn.run("src.main:app", host=host, port=port, reload=reload)
