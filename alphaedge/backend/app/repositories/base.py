"""Generic async repository base class for common CRUD operations."""

import uuid
from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, id: uuid.UUID) -> ModelType | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id, self.model.is_deleted == False)
        )
        return result.scalar_one_or_none()

    async def list_all(self, **filters) -> Sequence[ModelType]:
        query = select(self.model).where(self.model.is_deleted == False)
        for attr, value in filters.items():
            query = query.where(getattr(self.model, attr) == value)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, **kwargs) -> ModelType:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: ModelType, **kwargs) -> ModelType:
        for field, value in kwargs.items():
            setattr(instance, field, value)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def soft_delete(self, instance: ModelType) -> None:
        instance.is_deleted = True  # type: ignore[assignment]
        await self.session.flush()
