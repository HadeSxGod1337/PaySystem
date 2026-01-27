"""Concrete service implementation with logic"""

from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.base_service import BaseService

T = TypeVar("T")


class Service(BaseService[T]):
    """Concrete service implementation with basic logic"""

    def __init__(self, db: AsyncSession):
        """
        Initialize service

        Args:
            db: Database session
        """
        self.db = db

    async def refresh(self, entity: T) -> T:
        """
        Refresh entity from database

        Args:
            entity: Entity to refresh

        Returns:
            Refreshed entity
        """
        await self.db.refresh(entity)
        return entity
