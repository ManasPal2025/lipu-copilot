"""Quote item repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select

from app.models.quote_item import QuoteItem
from app.repositories.base import BaseRepository


class QuoteItemRepository(BaseRepository[QuoteItem]):
    model = QuoteItem

    async def get_for_quote(self, quote_id: UUID, item_id: UUID) -> QuoteItem | None:
        result = await self.session.execute(
            select(QuoteItem).where(QuoteItem.id == item_id, QuoteItem.quote_id == quote_id)
        )
        return result.scalar_one_or_none()

    async def list_for_quote(self, quote_id: UUID) -> Sequence[QuoteItem]:
        result = await self.session.execute(
            select(QuoteItem).where(QuoteItem.quote_id == quote_id).order_by(QuoteItem.created_at.asc())
        )
        return result.scalars().all()

    async def delete_for_quote(self, quote_id: UUID) -> None:
        for item in await self.list_for_quote(quote_id):
            await self.session.delete(item)
        await self.session.flush()

