from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal

from app.schemas.feature_schema import FeatureResponse


class PackageCreateRequest(BaseModel):
    """
    Schema dùng cho API tạo package.

    feature_ids là danh sách ID của features được gán cho package.
    Ví dụ:
    Basic có generate_image với id = 1
    => feature_ids = [1]
    """

    name: str
    description: Optional[str] = None
    price: Decimal
    credits: int
    feature_ids: List[int] = []


class PackageUpdateRequest(BaseModel):
    """
    Schema dùng cho API cập nhật package.

    Tất cả field đều Optional vì admin có thể chỉ sửa một vài thông tin.
    Nếu feature_ids = None thì không cập nhật features.
    Nếu feature_ids = [] thì package không còn feature nào.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    credits: Optional[int] = None
    is_active: Optional[bool] = None
    feature_ids: Optional[List[int]] = None


class PackageResponse(BaseModel):
    """
    Schema response trả package kèm danh sách features.

    Dùng để hiển thị package cho user chọn mua.
    """

    id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    credits: int
    is_active: bool
    features: List[FeatureResponse] = []

    class Config:
        from_attributes = True