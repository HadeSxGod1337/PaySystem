from decimal import Decimal

from pydantic import BaseModel


class AccountResponse(BaseModel):
    """Account data response schema"""

    id: int
    user_id: int
    balance: Decimal

    class Config:
        from_attributes = True
