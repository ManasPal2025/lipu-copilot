"""Product category repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select

from app.models.product_category import ProductCategory
from app.repositories.base import BaseRepository


class ProductCategoryRepository(BaseRepository[ProductCategory]):
    model = ProductCategory

    async def get_active(self, category_id: UUID) -> ProductCategory | None:
        result = await self.session.execute(select(ProductCategory).where(ProductCategory.id == category_id))
        return result.scalar_one_or_none()

    async def get_by_slug(self, organization_id: UUID, slug: str) -> ProductCategory | None:
        result = await self.session.execute(
            select(ProductCategory).where(
                ProductCategory.organization_id == organization_id,
                ProductCategory.slug == slug,
            )
        )
        return result.scalar_one_or_none()

    async def list_categories(
        self,
        *,
        organization_id: UUID | None = None,
        parent_category_id: UUID | None = None,
        is_active: bool | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[ProductCategory], int]:
        query = select(ProductCategory)
        count_query = select(func.count()).select_from(ProductCategory)

        filters = []
        if organization_id is not None:
            filters.append(ProductCategory.organization_id == organization_id)
        if parent_category_id is not None:
            filters.append(ProductCategory.parent_category_id == parent_category_id)
        if is_active is not None:
            filters.append(ProductCategory.is_active == is_active)

        if filters:
            query = query.where(*filters)
            count_query = count_query.where(*filters)

        total = await self.session.scalar(count_query)
        result = await self.session.execute(
            query.order_by(ProductCategory.display_order.asc(), ProductCategory.name.asc()).offset(offset).limit(limit)
        )
        return result.scalars().all(), int(total or 0)

