"""Generic repository primitives for SQLAlchemy models."""

from collections.abc import Sequence
from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import BaseModel


ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseRepository(Generic[ModelT]):
    """Base repository for simple persistence operations.

    Feature repositories should inherit from this and add domain-specific query
    methods. Route handlers should depend on services, not directly on this.
    """

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def base_query(self) -> Select[tuple[ModelT]]:
        return select(self.model)

    async def get(self, entity_id: UUID) -> ModelT | None:
        return await self.session.get(self.model, entity_id)

    async def list(self, *, offset: int = 0, limit: int = 100) -> Sequence[ModelT]:
        result = await self.session.execute(self.base_query().offset(offset).limit(limit))
        return result.scalars().all()

    async def create(self, **values: Any) -> ModelT:
        entity = self.model(**values)
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity: ModelT, **values: Any) -> ModelT:
        for key, value in values.items():
            setattr(entity, key, value)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity: ModelT) -> None:
        await self.session.delete(entity)
        await self.session.flush()

