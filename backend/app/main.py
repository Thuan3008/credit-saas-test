from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.models.user import User
from app.models.feature import Feature
from app.models.package import Package, PackageFeature

from app.routers.auth import router as auth_router
from app.routers.seed import router as seed_router
from app.routers.admin_test import router as admin_test_router
from app.routers.features import router as features_router
from app.routers.packages import router as packages_router

# Tạo bảng trong database nếu bảng chưa tồn tại
# Lưu ý: create_all không tự cập nhật cột nếu bảng đã tồn tại.
# Nếu đổi model mà database lỗi, cần docker-compose down -v
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Credit SaaS API",
    description="API for SaaS credit packages test assignment",
    version="1.0.0"
)


# CORS cho phép frontend React gọi API backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Demo test nên để *, production thì nên giới hạn domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Gắn các router vào FastAPI app
app.include_router(auth_router)
app.include_router(seed_router)
app.include_router(admin_test_router)
app.include_router(features_router)
app.include_router(packages_router)


@app.get("/")
def root():
    """
    API kiểm tra backend có chạy không.
    """

    return {
        "message": "Credit SaaS API is running"
    }


@app.get("/health")
def health_check():
    """
    API health check.
    Dùng để kiểm tra trạng thái backend.
    """

    return {
        "status": "ok"
    }