from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.feature import Feature
from app.models.user_credit import UserFeature
from app.dependencies.auth_dependency import get_current_user


def require_feature(feature_code: str):
    """
    Dependency kiểm tra user có quyền sử dụng một feature hay không.

    Cách dùng:
    user = Depends(require_feature("generate_image"))

    Flow kiểm tra:
    1. Lấy current_user từ JWT token
    2. Tìm feature theo feature_code
    3. Kiểm tra bảng user_features xem user đã unlock feature đó chưa
    4. Nếu chưa có quyền thì trả 403
    5. Nếu có quyền thì cho API chạy tiếp
    """

    def checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        """
        Hàm checker là dependency thật sự được FastAPI gọi.

        feature_code được truyền từ require_feature bên ngoài.
        Ví dụ:
        require_feature("auto_post")
        """

        # 1. Tìm feature theo code
        feature = db.query(Feature).filter(
            Feature.code == feature_code
        ).first()

        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feature not found: {feature_code}"
            )

        # 2. Kiểm tra user đã unlock feature này chưa
        user_feature = db.query(UserFeature).filter(
            UserFeature.user_id == current_user.id,
            UserFeature.feature_id == feature.id
        ).first()

        # 3. Nếu chưa unlock thì chặn API
        if not user_feature:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"You do not have permission to use feature: {feature_code}"
            )

        # 4. Nếu có quyền thì trả current_user để API bên dưới dùng tiếp
        return current_user

    return checker