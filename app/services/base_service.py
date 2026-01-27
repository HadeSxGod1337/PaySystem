"""Базовый абстрактный сервис"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseService(ABC, Generic[T]):
    """Абстрактный базовый сервис для бизнес-логики"""

    @abstractmethod
    async def refresh(self, entity: T) -> T:
        """
        Обновить сущность из базы данных

        Args:
            entity: Сущность для обновления

        Returns:
            Обновленная сущность
        """
        pass
