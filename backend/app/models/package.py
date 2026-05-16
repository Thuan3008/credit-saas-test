from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Package(Base):
    """
    Model Package đại diện cho bảng packages.
    Lưu thông tin các gói credits.
    """

    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    price = Column(Numeric(10, 2), nullable=False)

    credits = Column(Integer, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PackageFeature(Base):
    """
    Bảng trung gian package_features.

    Dùng để lưu quan hệ nhiều-nhiều giữa:
    - packages
    - features
    """

    __tablename__ = "package_features"

    id = Column(Integer, primary_key=True, index=True)

    package_id = Column(
        Integer,
        ForeignKey("packages.id", ondelete="CASCADE"),
        nullable=False
    )

    feature_id = Column(
        Integer,
        ForeignKey("features.id", ondelete="CASCADE"),
        nullable=False
    )