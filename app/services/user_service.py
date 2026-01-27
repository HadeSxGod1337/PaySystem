from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.error_messages import ErrorMessages
from app.core.security import get_password_hash
from app.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.models.account import Account
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.service import Service


class UserService(Service[User]):
    """Service for working with users"""

    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.user_repo = UserRepository()
        self.account_repo = AccountRepository()

    async def create_user(self, user_data: UserCreate) -> User:
        """Create user and automatically create account for them"""
        # Check if user with this email exists
        existing_user = await self.user_repo.get_by_email(self.db, user_data.email)
        if existing_user:
            raise UserAlreadyExistsError(
                message=ErrorMessages.USER_ALREADY_EXISTS, detail=ErrorMessages.USER_ALREADY_EXISTS
            )

        hashed_password = get_password_hash(user_data.password)
        user = await self.user_repo.create(self.db, user_data, hashed_password)

        # Automatically create account for new user with zero balance
        user_id: int = int(user.id)
        await self.account_repo.create(self.db, user_id, initial_balance=Decimal("0.00"))

        return user

    async def get_user(self, user_id: int) -> User:
        """Get user by ID"""
        user = await self.user_repo.get_by_id(self.db, user_id)
        if not user:
            raise UserNotFoundError(
                message=ErrorMessages.USER_NOT_FOUND, detail=ErrorMessages.USER_NOT_FOUND
            )
        return user

    async def get_user_accounts(self, user_id: int) -> list[Account]:
        """Get all user accounts"""
        accounts = await self.account_repo.get_by_user_id(self.db, user_id)
        return accounts

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Update user"""
        user = await self.get_user(user_id)

        # Check email uniqueness if it's being changed
        if user_data.email and user_data.email != user.email:
            existing_user = await self.user_repo.get_by_email(self.db, user_data.email)
            if existing_user:
                raise UserAlreadyExistsError(
                    message=ErrorMessages.USER_ALREADY_EXISTS,
                    detail=ErrorMessages.USER_ALREADY_EXISTS,
                )

        updated_user = await self.user_repo.update(self.db, user, user_data)
        return updated_user

    async def delete_user(self, user_id: int) -> None:
        """Delete user"""
        user = await self.get_user(user_id)
        await self.user_repo.delete(self.db, user)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all users list"""
        return await self.user_repo.get_all(self.db, skip, limit)
