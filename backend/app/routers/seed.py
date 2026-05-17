from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.feature import Feature
from app.models.package import Package, PackageFeature
from app.models.user_credit import UserCredit
from app.services.auth_service import hash_password


router = APIRouter(
    prefix="/api/seed",
    tags=["Seed"]
)


def get_or_create_user(
    db: Session,
    email: str,
    password: str,
    full_name: str,
    role: str
):
    """
    Hàm tạo user nếu chưa tồn tại.
    Nếu user đã tồn tại thì trả về user cũ.
    """

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user:
        return user

    user = User(
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_or_create_feature(
    db: Session,
    code: str,
    name: str,
    description: str
):
    """
    Hàm tạo feature nếu chưa tồn tại.
    """

    feature = db.query(Feature).filter(
        Feature.code == code
    ).first()

    if feature:
        return feature

    feature = Feature(
        code=code,
        name=name,
        description=description
    )

    db.add(feature)
    db.commit()
    db.refresh(feature)

    return feature


def get_or_create_package(
    db: Session,
    name: str,
    description: str,
    price: float,
    credits: int,
    feature_ids: list[int]
):
    """
    Hàm tạo package nếu chưa tồn tại.
    Sau đó gán features cho package.
    """

    package = db.query(Package).filter(
        Package.name == name
    ).first()

    if not package:
        package = Package(
            name=name,
            description=description,
            price=price,
            credits=credits,
            is_active=True
        )

        db.add(package)
        db.commit()
        db.refresh(package)

    # Xóa mapping cũ để tránh bị trùng feature
    db.query(PackageFeature).filter(
        PackageFeature.package_id == package.id
    ).delete()

    # Gán lại danh sách features
    for feature_id in feature_ids:
        db.add(PackageFeature(
            package_id=package.id,
            feature_id=feature_id
        ))

    db.commit()
    db.refresh(package)

    return package


@router.post("/admin")
def seed_admin(
    db: Session = Depends(get_db)
):
    """
    API tạo riêng admin demo.
    Giữ lại để tiện test nhanh.
    """

    admin = get_or_create_user(
        db=db,
        email="admin@example.com",
        password="123456",
        full_name="System Admin",
        role="admin"
    )

    return {
        "message": "Admin seed completed",
        "email": admin.email,
        "password": "123456"
    }


@router.post("/demo")
def seed_demo_data(
    db: Session = Depends(get_db)
):
    """
    API seed toàn bộ dữ liệu demo cho project.

    Bao gồm:
    - Admin account
    - Normal user account
    - Features
    - Credit packages
    """

    admin = get_or_create_user(
        db=db,
        email="admin@example.com",
        password="123456",
        full_name="System Admin",
        role="admin"
    )

    user = get_or_create_user(
        db=db,
        email="user@example.com",
        password="123456",
        full_name="Normal User",
        role="user"
    )

    # Tạo ví credits cho user demo nếu chưa có
    user_credit = db.query(UserCredit).filter(
        UserCredit.user_id == user.id
    ).first()

    if not user_credit:
        db.add(UserCredit(
            user_id=user.id,
            balance=0
        ))
        db.commit()

    generate_image = get_or_create_feature(
        db=db,
        code="generate_image",
        name="Generate Image",
        description="Allow user to generate AI images"
    )

    auto_post = get_or_create_feature(
        db=db,
        code="auto_post",
        name="Auto Post",
        description="Allow user to publish automatic posts"
    )

    advanced_analytics = get_or_create_feature(
        db=db,
        code="advanced_analytics",
        name="Advanced Analytics",
        description="Allow user to access advanced reports and analytics"
    )

    basic = get_or_create_package(
        db=db,
        name="Basic",
        description="Basic package for new users",
        price=9.99,
        credits=100,
        feature_ids=[
            generate_image.id
        ]
    )

    pro = get_or_create_package(
        db=db,
        name="Pro",
        description="Pro package for active users",
        price=29.99,
        credits=500,
        feature_ids=[
            generate_image.id,
            auto_post.id
        ]
    )

    enterprise = get_or_create_package(
        db=db,
        name="Enterprise",
        description="Enterprise package for teams",
        price=99.99,
        credits=2000,
        feature_ids=[
            generate_image.id,
            auto_post.id,
            advanced_analytics.id
        ]
    )

    return {
        "message": "Demo data seeded successfully",
        "accounts": {
            "admin": {
                "email": admin.email,
                "password": "123456"
            },
            "user": {
                "email": user.email,
                "password": "123456"
            }
        },
        "features": [
            generate_image.code,
            auto_post.code,
            advanced_analytics.code
        ],
        "packages": [
            basic.name,
            pro.name,
            enterprise.name
        ]
    }