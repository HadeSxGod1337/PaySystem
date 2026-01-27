"""Concrete repository implementation with logic"""

from typing import Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base
from app.repositories.base_repository import BaseRepository

T = TypeVar("T", bound=Base)


class Repository(BaseRepository[T]):
    """Concrete repository implementation with database logic"""

    def __init__(self, model: type[T]):
        """
        Initialize repository

        Args:
            model: SQLAlchemy model class
        """
        self.model = model

    async def get_by_id(self, db: AsyncSession, entity_id: int) -> Optional[T]:
        """
        Get entity by ID

        Args:
            db: Database session
            entity_id: Entity ID

        Returns:
            Entity or None if not found
        """
        result = await db.execute(select(self.model).where(self.model.id == entity_id))
        return result.scalar_one_or_none()

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
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, **kwargs) -> T:
        """
        Create new entity

        Args:
            db: Database session
            **kwargs: Parameters for entity creation

        Returns:
            Created entity
        """
        entity = self.model(**kwargs)
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
        return entity

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
        for key, value in kwargs.items():
            if value is not None and hasattr(entity, key):
                setattr(entity, key, value)
        await db.commit()
        await db.refresh(entity)
        return entity

    async def delete(self, db: AsyncSession, entity: T) -> None:
        """
        Delete entity

        Args:
            db: Database session
            entity: Entity to delete
        """
        await db.delete(entity)
        await db.commit()
