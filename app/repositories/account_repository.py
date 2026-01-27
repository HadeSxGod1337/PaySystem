from decimal import Decimal
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.repositories.repository import Repository


class AccountRepository(Repository[Account]):
    """Repository for working with accounts"""

    def __init__(self):
        super().__init__(Account)

    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> list[Account]:
        """Get all user accounts"""
        result = await db.execute(select(Account).where(Account.user_id == user_id))
        return list(result.scalars().all())

    async def get_by_user_and_account_id(
        self, db: AsyncSession, user_id: int, account_id: int
    ) -> Optional[Account]:
        """Get user account by account ID"""
        result = await db.execute(
            select(Account).where(Account.id == account_id, Account.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(  # type: ignore[override]
        self,
        db: AsyncSession,
        user_id: int,
        initial_balance: Decimal = Decimal("0.00"),
        account_id: Optional[int] = None,
    ) -> Account:
        """Create account for user"""
        account = Account(user_id=user_id, balance=initial_balance)
        if account_id is not None:
            account.id = account_id  # type: ignore[assignment]
        db.add(account)
        await db.commit()
        await db.refresh(account)
        return account

    async def update_balance(self, db: AsyncSession, account: Account, amount: Decimal) -> Account:
        """Update account balance (add amount)"""
        account.balance += amount  # type: ignore[assignment]
        await db.commit()
        await db.refresh(account)
        return account
