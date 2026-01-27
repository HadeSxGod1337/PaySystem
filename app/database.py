from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (  # type: ignore[attr-defined]
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase  # type: ignore[attr-defined]

from app.config import settings


class Base(DeclarativeBase):
    """Base class for all models"""

    pass


engine = create_async_engine(settings.database_url, echo=True, future=True)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
