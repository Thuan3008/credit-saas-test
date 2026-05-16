from sqlalchemy import Column, Integer, Numeric, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Transaction(Base):
    """
    Bảng transactions lưu lịch sử mua credits của user.

    Vì đề bài yêu cầu giả lập thanh toán,
    nên status có thể để success ngay sau khi mua.

    Status có thể là:
    - success
    - failed
    - pending
    """

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # User nào thực hiện giao dịch
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    # User mua package nào
    package_id = Column(
        Integer,
        ForeignKey("packages.id", ondelete="SET NULL"),
        nullable=True
    )

    # Số tiền thanh toán
    amount = Column(Numeric(10, 2), nullable=False)

    # Số credits được cộng
    credits = Column(Integer, nullable=False)

    # Trạng thái thanh toán
    status = Column(String, default="success", nullable=False)

    # Thời điểm tạo giao dịch
    created_at = Column(DateTime(timezone=True), server_default=func.now())