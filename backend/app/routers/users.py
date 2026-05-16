from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.user_credit import UserCredit, UserFeature
from app.models.feature import Feature
from app.dependencies.auth_dependency import get_current_user


router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)


@router.get("/me/credits")
def get_my_credits(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API xem số credits hiện tại của user.

    Nếu user chưa từng mua package,
    hệ thống trả balance = 0.
    """

    user_credit = db.query(UserCredit).filter(
        UserCredit.user_id == current_user.id
    ).first()

    if not user_credit:
        return {
            "balance": 0,
            "updated_at": None
        }

    return {
        "balance": user_credit.balance,
        "updated_at": user_credit.updated_at
    }


@router.get("/me/features")
def get_my_features(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API xem danh sách features user đã unlock.

    Dùng cho frontend dashboard:
    - Generate Image
    - Auto Post
    - Advanced Analytics
    """

    user_features = db.query(UserFeature).filter(
        UserFeature.user_id == current_user.id
    ).all()

    feature_ids = [
        user_feature.feature_id
        for user_feature in user_features
    ]

    if not feature_ids:
        return []

    features = db.query(Feature).filter(
        Feature.id.in_(feature_ids)
    ).all()

    return features