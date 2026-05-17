from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# Import models để SQLAlchemy biết những bảng cần tạo
from app.models.user import User
from app.models.feature import Feature
from app.models.package import Package, PackageFeature
from app.models.user_credit import UserCredit, UserFeature
from app.models.transaction import Transaction

# Import routers
from app.routers.auth import router as auth_router
from app.routers.seed import router as seed_router
from app.routers.admin_test import router as admin_test_router
from app.routers.features import router as features_router
from app.routers.packages import router as packages_router
from app.routers.purchases import router as purchases_router
from app.routers.users import router as users_router

from app.routers.feature_usage import router as feature_usage_router

# Tạo bảng nếu chưa tồn tại
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Credit SaaS API",
    description="API for SaaS credit packages test assignment",
    version="1.0.0"
)


# Cho phép frontend React gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Gắn router vào app
app.include_router(auth_router)
app.include_router(seed_router)
app.include_router(admin_test_router)
app.include_router(features_router)
app.include_router(packages_router)
app.include_router(purchases_router)
app.include_router(users_router)
app.include_router(feature_usage_router)

@app.get("/")
def root():
    return {
        "message": "Credit SaaS API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }