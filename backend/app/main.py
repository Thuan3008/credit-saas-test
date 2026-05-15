from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

from app.models.user import User

from app.routers.auth import router as auth_router

from app.routers.auth import router as auth_router
from app.routers.seed import router as seed_router

from app.routers.admin_test import router as admin_test_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Credit SaaS API",
    description="API for SaaS credit packages test assignment",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)

app.include_router(auth_router)
app.include_router(seed_router)

app.include_router(admin_test_router)

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