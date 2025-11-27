from fastapi import FastAPI
import uvicorn

from src.boostrap.middleware import register_middlewares
from src.boostrap.migration import run_migrations
from src.boostrap.seeds import run_seeds
from src.boostrap.register import setup_routes
from src.shared.auth.openapi import apply_security_scheme
from src.shared.constants.server import SERVER_HOST, SERVER_PORT, SERVER_RELOAD


def create_app() -> FastAPI:
    app = FastAPI(
        title="Backend API",
        version="0.1.0",
        description=(
            "# Backend Service\n"
            "- Quản lý sample feature với endpoint `/hello`\n"
            "- Theo dõi sức khỏe hệ thống qua `/health`\n"
            "\n"
            "## Hướng dẫn\n"
            "Sử dụng Swagger tại `/swagger` hoặc ReDoc tại `/redoc` để khám phá API."
        ),
        docs_url="/swagger",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    register_middlewares(app)
    run_migrations()
    setup_routes(app)
    run_seeds()
    apply_security_scheme(app)
    return app


def run_server() -> None:
    uvicorn.run(
        "src.boostrap.app:create_app",
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=SERVER_RELOAD,
        factory=True,
    )

