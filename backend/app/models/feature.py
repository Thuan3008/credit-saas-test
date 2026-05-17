from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Feature(Base):
    """
    Model Feature đại diện cho bảng features trong database.

    Bảng này lưu các tính năng mà user có thể được unlock
    sau khi mua một package nào đó.

    Ví dụ:
    - generate_image
    - auto_post
    - advanced_analytics
    """

    __tablename__ = "features"

    # Khóa chính của bảng features
    id = Column(Integer, primary_key=True, index=True)

    # Mã tính năng, dùng để check quyền trong middleware sau này
    # Ví dụ: generate_image, auto_post
    # unique=True để không bị trùng code
    code = Column(String, unique=True, index=True, nullable=False)

    # Tên hiển thị của tính năng
    # Ví dụ: Generate Image, Auto Post
    name = Column(String, nullable=False)

    # Mô tả chi tiết tính năng
    description = Column(Text, nullable=True)