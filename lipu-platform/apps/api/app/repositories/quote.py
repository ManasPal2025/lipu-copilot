"""Quote repository."""

from collections.abc import Sequence
from datetime import date
from uuid import UUID

from sqlalchemy import Select, and_, desc, func, select
from sqlalchemy.orm import selectinload

from app.models.quote import Quote
from app.repositories.base import BaseRepository


class QuoteRepository(BaseRepository[Quote]):
    model = Quote

    SORT_COLUMNS = {
        "created_at": Quote.created_at,
        "valid_until": Quote.valid_until,
        "total_amount": Quote.total_amount,
    }

    async def get_active(self, quote_id: UUID, *, include_items: bool = False) -> Quote | None:
        query = select(Quote).where(Quote.id == quote_id, Quote.deleted_at.is_(None))
        if include_items:
            query = query.options(selectinload(Quote.items))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_number(self, quote_number: str) -> Quote | None:
        result = await self.session.execute(
            select(Quote).where(Quote.quote_number == quote_number, Quote.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def list_quotes(
        self,
        *,
        organization_id: UUID | None = None,
        customer_id: UUID | None = None,
        status: str | None = None,
        valid_from: date | None = None,
        valid_to: date | None = None,
        sort: str = "-created_at",
        offset: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[Quote], int]:
        filters = [Quote.deleted_at.is_(None)]
        if organization_id is not None:
            filters.append(Quote.organization_id == organization_id)
        if customer_id is not None:
            filters.append(Quote.customer_id == customer_id)
        if status is not None:
            filters.append(Quote.status == status)
        if valid_from is not None:
            filters.append(Quote.valid_until >= valid_from)
        if valid_to is not None:
            filters.append(Quote.valid_until <= valid_to)

        query: Select[tuple[Quote]] = select(Quote).where(and_(*filters))
        count_query = select(func.count()).select_from(Quote).where(and_(*filters))
        query = self._apply_sort(query, sort)

        total = await self.session.scalar(count_query)
        result = await self.session.execute(query.offset(offset).limit(limit))
        return result.scalars().all(), int(total or 0)

    def _apply_sort(self, query: Select[tuple[Quote]], sort: str) -> Select[tuple[Quote]]:
        descending = sort.startswith("-")
        key = sort[1:] if descending else sort
        column = self.SORT_COLUMNS.get(key, Quote.created_at)
        return query.order_by(desc(column) if descending else column.asc())

