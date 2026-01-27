from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.payment import WebhookRequest
from app.services.payment_service import PaymentService

router = APIRouter()


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def process_payment_webhook(
    webhook_data: WebhookRequest, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Process webhook from payment system"""
    service = PaymentService(db)
    result = await service.process_webhook(webhook_data)
    return result
