from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PaymentResponse(BaseModel):
    """Payment data response schema"""

    id: int
    transaction_id: str
    user_id: int
    account_id: int
    amount: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


class WebhookRequest(BaseModel):
    """Webhook request schema from payment system"""

    transaction_id: str
    account_id: int
    user_id: int
    amount: Decimal
    signature: str
