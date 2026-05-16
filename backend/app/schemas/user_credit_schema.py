from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreditResponse(BaseModel):
    """
    Schema trả số credits hiện tại của user.
    """

    balance: int
    updated_at: Optional[datetime] = None


class UserFeatureResponse(BaseModel):
    """
    Schema trả feature mà user đã unlock.
    """

    id: int
    code: str
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True