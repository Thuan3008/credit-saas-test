from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.package import Package, PackageFeature
from app.models.feature import Feature
from app.schemas.package_schema import (
    PackageCreateRequest,
    PackageUpdateRequest
)
from app.dependencies.auth_dependency import require_admin


router = APIRouter(
    prefix="/api/packages",
    tags=["Packages"]
)


def build_package_response(package: Package, db: Session):
    """
    Hàm này dùng để build response package kèm danh sách features.

    Lý do cần hàm này:
    - Bảng packages chỉ chứa thông tin package
    - Bảng features chứa thông tin feature
    - Bảng package_features là bảng trung gian
    => Muốn trả package kèm features thì phải query thêm.
    """

    # Lấy danh sách quan hệ package-feature của package hiện tại
    package_features = db.query(PackageFeature).filter(
        PackageFeature.package_id == package.id
    ).all()

    # Tách ra danh sách feature_id
    feature_ids = [
        item.feature_id
        for item in package_features
    ]

    features = []

    # Nếu package có feature thì query thông tin feature
    if feature_ids:
        features = db.query(Feature).filter(
            Feature.id.in_(feature_ids)
        ).all()

    # Trả về dict để FastAPI tự convert sang JSON
    return {
        "id": package.id,
        "name": package.name,
        "description": package.description,
        "price": package.price,
        "credits": package.credits,
        "is_active": package.is_active,
        "features": features
    }


@router.get("")
def get_packages(
    db: Session = Depends(get_db)
):
    """
    API lấy danh sách package cho user xem.

    Chỉ trả các package đang active.
    Package bị soft delete sẽ không hiện ở đây.
    API này không cần đăng nhập.
    """

    packages = db.query(Package).filter(
        Package.is_active == True
    ).order_by(Package.price.asc()).all()

    return [
        build_package_response(package, db)
        for package in packages
    ]


@router.get("/admin")
def get_packages_for_admin(
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """
    API lấy danh sách package cho admin.

    Admin xem được cả package active và inactive.
    Dùng cho màn hình quản lý package.
    """

    packages = db.query(Package).order_by(
        Package.id.asc()
    ).all()

    return [
        build_package_response(package, db)
        for package in packages
    ]


@router.get("/{package_id}")
def get_package_detail(
    package_id: int,
    db: Session = Depends(get_db)
):
    """
    API lấy chi tiết một package.

    User chỉ xem được package đang active.
    """

    package = db.query(Package).filter(
        Package.id == package_id,
        Package.is_active == True
    ).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    return build_package_response(package, db)


@router.post("")
def create_package(
    request: PackageCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """
    API tạo package mới.

    Chỉ admin được phép tạo package.
    Khi tạo package có thể gán luôn danh sách feature_ids.
    """

    # Tạo package trước
    package = Package(
        name=request.name,
        description=request.description,
        price=request.price,
        credits=request.credits,
        is_active=True
    )

    db.add(package)
    db.commit()
    db.refresh(package)

    # Sau khi có package.id, bắt đầu gán features cho package
    for feature_id in request.feature_ids:
        # Kiểm tra feature_id có tồn tại không
        feature = db.query(Feature).filter(
            Feature.id == feature_id
        ).first()

        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feature with id {feature_id} not found"
            )

        # Tạo record trong bảng trung gian package_features
        package_feature = PackageFeature(
            package_id=package.id,
            feature_id=feature_id
        )

        db.add(package_feature)

    db.commit()

    return build_package_response(package, db)


@router.put("/{package_id}")
def update_package(
    package_id: int,
    request: PackageUpdateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """
    API cập nhật package.

    Chỉ admin được phép cập nhật.
    Có thể cập nhật:
    - name
    - description
    - price
    - credits
    - is_active
    - feature_ids
    """

    # Tìm package cần sửa
    package = db.query(Package).filter(
        Package.id == package_id
    ).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    # Chỉ cập nhật field nào được gửi lên
    if request.name is not None:
        package.name = request.name

    if request.description is not None:
        package.description = request.description

    if request.price is not None:
        package.price = request.price

    if request.credits is not None:
        package.credits = request.credits

    if request.is_active is not None:
        package.is_active = request.is_active

    # Nếu request có gửi feature_ids thì cập nhật lại toàn bộ features của package
    if request.feature_ids is not None:
        # Xóa danh sách feature cũ của package
        db.query(PackageFeature).filter(
            PackageFeature.package_id == package.id
        ).delete()

        # Thêm danh sách feature mới
        for feature_id in request.feature_ids:
            feature = db.query(Feature).filter(
                Feature.id == feature_id
            ).first()

            if not feature:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Feature with id {feature_id} not found"
                )

            db.add(PackageFeature(
                package_id=package.id,
                feature_id=feature_id
            ))

    db.commit()
    db.refresh(package)

    return build_package_response(package, db)


@router.delete("/{package_id}")
def delete_package(
    package_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """
    API xóa package.

    Ở đây không xóa thật khỏi database.
    Mình dùng soft delete bằng cách set is_active = False.

    Lý do:
    - Giữ được lịch sử giao dịch sau này
    - Admin vẫn xem được package cũ
    - User không thấy package đã bị ẩn
    """

    package = db.query(Package).filter(
        Package.id == package_id
    ).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    # Soft delete
    package.is_active = False

    db.commit()

    return {
        "message": "Package deleted successfully"
    }