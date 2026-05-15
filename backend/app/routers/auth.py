from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse
)
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)
from app.dependencies.auth_dependency import get_current_user


router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserResponse)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    existed_user = db.query(User).filter(
        User.email == request.email
    ).first()

    if existed_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        email=request.email,
        full_name=request.full_name,
        password_hash=hash_password(request.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user