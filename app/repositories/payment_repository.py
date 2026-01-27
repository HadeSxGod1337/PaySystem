from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.payment import Payment
from app.repositories.repository import Repository


class PaymentRepository(Repository[Payment]):
    """Repository for working with payments"""

    def __init__(self):
        super().__init__(Payment)

    async def get_by_transaction_id(
        self, db: AsyncSession, transaction_id: str
    ) -> Optional[Payment]:
        """Get payment by transaction_id"""
        result = await db.execute(select(Payment).where(Payment.transaction_id == transaction_id))
        return result.scalar_one_or_none()

    async def get_by_user_id(
        self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Payment]:
        """Get all user payments"""
        result = await db.execute(
            select(Payment)
            .where(Payment.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Payment.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(  # type: ignore[override]
        self, db: AsyncSession, transaction_id: str, user_id: int, account_id: int, amount: Decimal
    ) -> Payment:
        """Create payment"""
        return await super().create(
            db, transaction_id=transaction_id, user_id=user_id, account_id=account_id, amount=amount
        )
