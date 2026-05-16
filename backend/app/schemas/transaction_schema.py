from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class TransactionResponse(BaseModel):
    """
    Schema trả lịch sử giao dịch ra client.
    """

    id: int
    user_id: int
    package_id: int | None
    amount: Decimal
    credits: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True