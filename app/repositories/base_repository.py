"""Base abstract repository"""

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base

T = TypeVar("T", bound=Base)


class BaseRepository(ABC, Generic[T]):
    """Abstract base repository for working with models"""

    @abstractmethod
    async def get_by_id(self, db: AsyncSession, entity_id: int) -> Optional[T]:
        """
        Get entity by ID

        Args:
            db: Database session
            entity_id: Entity ID

        Returns:
            Entity or None if not found
        """
        pass

    @abstractmethod
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[T]:
        """
        Get all entities list

        Args:
            db: Database session
            skip: Number of skipped records
            limit: Maximum number of records

        Returns:
            List of entities
        """
        pass

    @abstractmethod
    async def create(self, db: AsyncSession, **kwargs) -> T:
        """
        Create new entity

        Args:
            db: Database session
            **kwargs: Parameters for entity creation

        Returns:
            Created entity
        """
        pass

    @abstractmethod
    async def update(self, db: AsyncSession, entity: T, **kwargs) -> T:
        """
        Update entity

        Args:
            db: Database session
            entity: Entity to update
            **kwargs: Fields to update

        Returns:
            Updated entity
        """
        pass

    @abstractmethod
    async def delete(self, db: AsyncSession, entity: T) -> None:
        """
        Delete entity

        Args:
            db: Database session
            entity: Entity to delete
        """
        pass
