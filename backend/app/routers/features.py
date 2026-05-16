from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.feature import Feature
from app.schemas.feature_schema import (
    FeatureCreateRequest,
    FeatureUpdateRequest,
    FeatureResponse
)
from app.dependencies.auth_dependency import require_admin


router = APIRouter(
    prefix="/api/features",
    tags=["Features"]
)


@router.get("", response_model=list[FeatureResponse])
def get_features(
    db: Session = Depends(get_db)
):
    """
    API lấy danh sách tất cả features.

    API này cho phép user/admin đều xem được.
    Dùng để hiển thị danh sách tính năng.
    """

    features = db.query(Feature).order_by(Feature.id.asc()).all()
    return features


@router.post("", response_model=FeatureResponse)
def create_feature(
    request: FeatureCreateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """
    API tạo feature mới.

    Chỉ admin được phép tạo feature.
    Ví dụ tạo feature:
    - generate_image
    - auto_post
    - advanced_analytics
    """

    # Kiểm tra code feature đã tồn tại chưa
    existed_feature = db.query(Feature).filter(
        Feature.code == request.code
    ).first()

    if existed_feature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feature code already exists"
        )

    # Tạo object Feature mới
    feature = Feature(
        code=request.code,
        name=request.name,
        description=request.description
    )

    # Lưu vào database
    db.add(feature)
    db.commit()
    db.refresh(feature)

    return feature


@router.put("/{feature_id}", response_model=FeatureResponse)
def update_feature(
    feature_id: int,
    request: FeatureUpdateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """
    API cập nhật feature.

    Chỉ admin được phép sửa.
    Có thể sửa code, name, description.
    """

    # Tìm feature theo id
    feature = db.query(Feature).filter(
        Feature.id == feature_id
    ).first()

    if not feature:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feature not found"
        )

    # Nếu admin muốn đổi code thì cần kiểm tra code mới có bị trùng không
    if request.code is not None:
        existed_code = db.query(Feature).filter(
            Feature.code == request.code,
            Feature.id != feature_id
        ).first()

        if existed_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feature code already exists"
            )

        feature.code = request.code

    # Cập nhật name nếu request có gửi name
    if request.name is not None:
        feature.name = request.name

    # Cập nhật description nếu request có gửi description
    if request.description is not None:
        feature.description = request.description

    db.commit()
    db.refresh(feature)

    return feature


@router.delete("/{feature_id}")
def delete_feature(
    feature_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """
    API xóa feature.

    Chỉ admin được phép xóa.
    Lưu ý: Nếu feature đã được gán cho package,
    package_features liên quan sẽ bị xóa theo do ondelete='CASCADE'.
    """

    feature = db.query(Feature).filter(
        Feature.id == feature_id
    ).first()

    if not feature:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feature not found"
        )

    db.delete(feature)
    db.commit()

    return {
        "message": "Feature deleted successfully"
    }