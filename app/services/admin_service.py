from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_messages import ErrorMessages
from app.exceptions import AdminNotFoundError
from app.models.account import Account
from app.models.user import Admin
from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import AdminRepository
from app.services.service import Service


class AdminService(Service[Admin]):
    """Service for working with admins"""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.admin_repo = AdminRepository()
        self.account_repo = AccountRepository()

    async def get_admin(self, admin_id: int) -> Admin:
        """Get admin by ID"""
        admin = await self.admin_repo.get_by_id(self.db, admin_id)
        if not admin:
            raise AdminNotFoundError(
                message=ErrorMessages.ADMIN_NOT_FOUND, detail=ErrorMessages.ADMIN_NOT_FOUND
            )
        return admin

    async def get_user_accounts(self, user_id: int) -> list[Account]:
        """Get all user accounts (for admin)"""
        accounts = await self.account_repo.get_by_user_id(self.db, user_id)
        return accounts
