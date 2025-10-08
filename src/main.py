from fastapi import FastAPI
from src.route.auth_route import router as auth_router
from src.route.bottle_route import router as bottle_router
from src.helper.settings_helper import load_settings
from fastapi.openapi.utils import get_openapi
import logging
from src.middleware.health_admin_middleware import HealthAdminMiddleware
from src.middleware.api_auth_middleware import ApiAuthMiddleware
from src.bootstrap import init_db
from src.bootstrap import init_routes

settings = load_settings()
server_cfg = settings.get("server", {})

openapi_tags = [
    {"name": "Health", "description": "Health check endpoints"},
    {"name": "Auth", "description": "Authentication endpoints"},
]

app = FastAPI(title="BTL Mobile Backend", version="0.1.0", openapi_tags=openapi_tags)

app.add_middleware(HealthAdminMiddleware)
app.add_middleware(ApiAuthMiddleware)
app.include_router(auth_router)
app.include_router(bottle_router)
init_routes(app)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})[
        "BearerAuth"
    ] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

try:
    init_db()
except Exception as e:
    logging.getLogger("app").error("startup failed: %s", str(e))


if __name__ == "__main__":
    import uvicorn

    host = server_cfg.get("host", "127.0.0.1")
    port = int(server_cfg.get("port", 8000))
    reload = bool(server_cfg.get("reload", False))
    uvicorn.run("src.main:app", host=host, port=port, reload=reload)
