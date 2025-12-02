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
            "# Backend API Documentation\n\n"
            "API backend cho ứng dụng quản lý bottle messages.\n\n"
            "## Tính năng chính\n\n"
            "### Authentication\n"
            "- **POST /auth/register**: Đăng ký tài khoản mới\n"
            "- **POST /auth/login**: Đăng nhập và nhận JWT token\n\n"
            "### Public Bottles (Sea)\n"
            "- **POST /sea/bottle**: Tạo bottle mới (có thể ẩn danh)\n"
            "- **GET /sea/bottle**: Lấy ngẫu nhiên một bottle từ biển\n\n"
            "### Stored Bottles (API)\n"
            "- **POST /api/store-bottle**: Lưu bottle vào danh sách của user\n"
            "- **GET /api/store-bottle**: Lấy danh sách bottles đã lưu (phân trang)\n"
            "- **GET /api/store-bottle/{stored_bottle_id}**: Lấy chi tiết stored bottle\n"
            "- **DELETE /api/store-bottle/{stored_bottle_id}**: Xóa stored bottle\n\n"
            "### User Info\n"
            "- **GET /api/me**: Lấy thông tin user hiện tại\n\n"
            "### Health Check\n"
            "- **GET /health**: Kiểm tra trạng thái hệ thống\n\n"
            "## Xác thực\n\n"
            "Hầu hết các endpoint API yêu cầu JWT token trong header:\n"
            "```\n"
            "Authorization: Bearer <token>\n"
            "```\n\n"
            "Token được lấy từ endpoint `/auth/login` sau khi đăng nhập thành công.\n\n"
            "## Hướng dẫn sử dụng\n\n"
            "1. Sử dụng Swagger UI tại `/swagger` để test API trực tiếp\n"
            "2. Sử dụng ReDoc tại `/redoc` để xem documentation chi tiết\n"
            "3. Click nút **Authorize** trong Swagger để nhập JWT token\n"
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

