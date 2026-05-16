from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from app.database import Base


class UserCredit(Base):
    """
    Bảng user_credits lưu số credits hiện tại của từng user.

    Mỗi user chỉ có một record trong bảng này.
    Ví dụ:
    user_id = 1
    balance = 500
    """

    __tablename__ = "user_credits"

    id = Column(Integer, primary_key=True, index=True)

    # Mỗi user chỉ có một ví credits
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    # Số credits hiện tại của user
    balance = Column(Integer, default=0, nullable=False)

    # Thời gian cập nhật gần nhất
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class UserFeature(Base):
    """
    Bảng user_features lưu các tính năng user đã unlock.

    Khi user mua package, hệ thống sẽ lấy features của package
    rồi thêm vào bảng này.

    Ví dụ:
    user_id = 1 unlock feature_id = 1 generate_image
    user_id = 1 unlock feature_id = 2 auto_post
    """

    __tablename__ = "user_features"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    feature_id = Column(
        Integer,
        ForeignKey("features.id", ondelete="CASCADE"),
        nullable=False
    )

    unlocked_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Không cho một user unlock trùng một feature nhiều lần
    __table_args__ = (
        UniqueConstraint("user_id", "feature_id", name="unique_user_feature"),
    )