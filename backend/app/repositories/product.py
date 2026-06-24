"""Product repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import Select, and_, desc, func, or_, select
from sqlalchemy.orm import selectinload

from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    model = Product

    SORT_COLUMNS = {
        "created_at": Product.created_at,
        "name": Product.name,
        "base_price": Product.base_price,
        "display_order": Product.display_order,
    }

    async def get_active(self, product_id: UUID, *, include_variants: bool = False) -> Product | None:
        query = select(Product).where(Product.id == product_id, Product.deleted_at.is_(None))
        if include_variants:
            query = query.options(selectinload(Product.variants))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_slug(self, organization_id: UUID, slug: str) -> Product | None:
        result = await self.session.execute(
            select(Product).where(
                Product.organization_id == organization_id,
                Product.slug == slug,
                Product.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_sku(self, organization_id: UUID, sku: str) -> Product | None:
        result = await self.session.execute(
            select(Product).where(
                Product.organization_id == organization_id,
                Product.sku == sku,
                Product.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def count_by_category(self, category_id: UUID) -> int:
        total = await self.session.scalar(
            select(func.count()).select_from(Product).where(Product.category_id == category_id, Product.deleted_at.is_(None))
        )
        return int(total or 0)

    async def list_products(
        self,
        *,
        organization_id: UUID | None = None,
        category_id: UUID | None = None,
        status: str | None = None,
        visibility: str | None = None,
        is_bestseller: bool | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        search: str | None = None,
        sort: str = "-created_at",
        offset: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[Product], int]:
        filters = [Product.deleted_at.is_(None)]
        if organization_id is not None:
            filters.append(Product.organization_id == organization_id)
        if category_id is not None:
            filters.append(Product.category_id == category_id)
        if status is not None:
            filters.append(Product.status == status)
        if visibility is not None:
            filters.append(Product.visibility == visibility)
        if is_bestseller is not None:
            filters.append(Product.is_bestseller == is_bestseller)
        if min_price is not None:
            filters.append(Product.base_price >= min_price)
        if max_price is not None:
            filters.append(Product.base_price <= max_price)

        query: Select[tuple[Product]] = select(Product).where(and_(*filters))
        count_query = select(func.count()).select_from(Product).where(and_(*filters))

        if search:
            ts_query = func.websearch_to_tsquery("english", search)
            search_filter = or_(
                Product.search_text.op("@@")(ts_query),
                Product.name.ilike(f"%{search}%"),
                Product.sku.ilike(f"%{search}%"),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)
            query = query.order_by(desc(func.ts_rank_cd(Product.search_text, ts_query)))

        query = self._apply_sort(query, sort)
        total = await self.session.scalar(count_query)
        result = await self.session.execute(query.offset(offset).limit(limit))
        return result.scalars().all(), int(total or 0)

    def _apply_sort(self, query: Select[tuple[Product]], sort: str) -> Select[tuple[Product]]:
        descending = sort.startswith("-")
        key = sort[1:] if descending else sort
        column = self.SORT_COLUMNS.get(key, Product.created_at)
        return query.order_by(desc(column) if descending else column.asc())
