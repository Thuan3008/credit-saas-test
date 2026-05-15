from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth_service import hash_password


router = APIRouter(
    prefix="/api/seed",
    tags=["Seed"]
)


@router.post("/admin")
def seed_admin(
    db: Session = Depends(get_db)
):
    existed_admin = db.query(User).filter(
        User.email == "admin@example.com"
    ).first()

    if existed_admin:
        return {
            "message": "Admin already exists",
            "email": existed_admin.email
        }

    admin = User(
        email="admin@example.com",
        full_name="System Admin",
        password_hash=hash_password("123456"),
        role="admin"
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return {
        "message": "Admin created successfully",
        "email": admin.email,
        "password": "123456"
    }