from pydantic import BaseModel
from typing import Optional


class FeatureCreateRequest(BaseModel):
    """
    Schema dùng cho API tạo feature.

    Client cần gửi:
    - code
    - name
    - description nếu có
    """

    code: str
    name: str
    description: Optional[str] = None


class FeatureUpdateRequest(BaseModel):
    """
    Schema dùng cho API cập nhật feature.

    Tất cả field đều Optional vì admin có thể chỉ sửa 1 field.
    Ví dụ chỉ sửa name, không cần gửi lại code.
    """

    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None


class FeatureResponse(BaseModel):
    """
    Schema response trả feature ra ngoài client.

    Không trả dữ liệu nhạy cảm.
    Chỉ trả các field cần hiển thị.
    """

    id: int
    code: str
    name: str
    description: Optional[str] = None

    class Config:
        # Cho phép Pydantic convert từ SQLAlchemy model sang response
        from_attributes = True