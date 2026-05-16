from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.package import Package, PackageFeature
from app.models.user_credit import UserCredit, UserFeature
from app.models.transaction import Transaction
from app.dependencies.auth_dependency import get_current_user


router = APIRouter(
    prefix="/api/purchases",
    tags=["Purchases"]
)


@router.post("/{package_id}")
def purchase_package(
    package_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API mua package credits.

    Flow:
    1. User chọn package
    2. Backend kiểm tra package có tồn tại và đang active không
    3. Giả lập thanh toán thành công
    4. Tạo transaction status = success
    5. Cộng credits vào ví user
    6. Unlock features thuộc package
    7. Trả kết quả về client
    """

    # 1. Tìm package user muốn mua
    package = db.query(Package).filter(
        Package.id == package_id,
        Package.is_active == True
    ).first()

    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )

    # 2. Tạo transaction giả lập thanh toán thành công
    transaction = Transaction(
        user_id=current_user.id,
        package_id=package.id,
        amount=package.price,
        credits=package.credits,
        status="success"
    )

    db.add(transaction)

    # 3. Lấy ví credits của user
    user_credit = db.query(UserCredit).filter(
        UserCredit.user_id == current_user.id
    ).first()

    # Nếu user chưa có ví credits thì tạo mới
    if not user_credit:
        user_credit = UserCredit(
            user_id=current_user.id,
            balance=0
        )
        db.add(user_credit)
        db.flush()

    # 4. Cộng credits vào ví
    user_credit.balance += package.credits

    # 5. Lấy danh sách features của package
    package_features = db.query(PackageFeature).filter(
        PackageFeature.package_id == package.id
    ).all()

    unlocked_feature_ids = []

    # 6. Unlock từng feature cho user
    for package_feature in package_features:
        existed_user_feature = db.query(UserFeature).filter(
            UserFeature.user_id == current_user.id,
            UserFeature.feature_id == package_feature.feature_id
        ).first()

        # Nếu user chưa có feature này thì thêm vào
        if not existed_user_feature:
            db.add(UserFeature(
                user_id=current_user.id,
                feature_id=package_feature.feature_id
            ))
            unlocked_feature_ids.append(package_feature.feature_id)

    db.commit()
    db.refresh(transaction)
    db.refresh(user_credit)

    return {
        "message": "Purchase successful",
        "transaction_id": transaction.id,
        "package_id": package.id,
        "package_name": package.name,
        "amount": package.price,
        "credits_added": package.credits,
        "current_balance": user_credit.balance,
        "unlocked_feature_ids": unlocked_feature_ids
    }


@router.get("/history")
def get_purchase_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    API lấy lịch sử mua credits của user hiện tại.

    User chỉ xem được giao dịch của chính mình.
    """

    transactions = db.query(Transaction).filter(
        Transaction.user_id == current_user.id
    ).order_by(
        Transaction.created_at.desc()
    ).all()

    return transactions