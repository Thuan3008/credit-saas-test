from fastapi import APIRouter, Depends

from app.dependencies.auth_dependency import require_admin
from app.models.user import User


router = APIRouter(
    prefix="/api/admin",
    tags=["Admin Test"]
)


@router.get("/only")
def admin_only(
    current_user: User = Depends(require_admin)
):
    return {
        "message": "You are admin",
        "email": current_user.email,
        "role": current_user.role
    }