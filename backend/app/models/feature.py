from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)

    # code dùng để check quyền sau này, ví dụ: generate_image, auto_post
    code = Column(String, unique=True, index=True, nullable=False)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)