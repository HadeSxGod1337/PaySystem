from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import Admin, User
from app.repositories.repository import Repository
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(Repository[User]):
    """Repository for working with users"""

    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(  # type: ignore[override]
        self, db: AsyncSession, user_data: UserCreate, hashed_password: str
    ) -> User:
        """Create user"""
        return await super().create(
            db,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )

    async def update(  # type: ignore[override]
        self, db: AsyncSession, user: User, user_data: UserUpdate
    ) -> User:
        """Update user"""
        update_data: dict = {}
        if user_data.email is not None:
            update_data["email"] = user_data.email
        if user_data.full_name is not None:
            update_data["full_name"] = user_data.full_name
        if user_data.password is not None:
            update_data["hashed_password"] = get_password_hash(user_data.password)
        if user_data.is_active is not None:
            update_data["is_active"] = bool(user_data.is_active)

        return await super().update(db, user, **update_data)


class AdminRepository(Repository[Admin]):
    """Repository for working with admins"""

    def __init__(self):
        super().__init__(Admin)

    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[Admin]:
        """Get admin by email"""
        result = await db.execute(select(Admin).where(Admin.email == email))
        return result.scalar_one_or_none()
