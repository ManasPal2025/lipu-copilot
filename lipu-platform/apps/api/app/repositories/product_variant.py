"""Product variant repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, or_, select

from app.models.product_variant import ProductVariant
from app.repositories.base import BaseRepository


class ProductVariantRepository(BaseRepository[ProductVariant]):
    model = ProductVariant

    async def get_by_id(self, variant_id: UUID) -> ProductVariant | None:
        result = await self.session.execute(select(ProductVariant).where(ProductVariant.id == variant_id))
        return result.scalar_one_or_none()

    async def get_by_value(self, product_id: UUID, variant_type: str, variant_value: str) -> ProductVariant | None:
        result = await self.session.execute(
            select(ProductVariant).where(
                ProductVariant.product_id == product_id,
                ProductVariant.variant_type == variant_type,
                ProductVariant.variant_value == variant_value,
            )
        )
        return result.scalar_one_or_none()

    async def list_variants(
        self,
        *,
        product_id: UUID,
        variant_type: str | None = None,
        is_available: bool | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> tuple[Sequence[ProductVariant], int]:
        query = select(ProductVariant).where(ProductVariant.product_id == product_id)
        count_query = select(func.count()).select_from(ProductVariant).where(ProductVariant.product_id == product_id)

        if variant_type is not None:
            query = query.where(ProductVariant.variant_type == variant_type)
            count_query = count_query.where(ProductVariant.variant_type == variant_type)
        if is_available is not None:
            query = query.where(ProductVariant.is_available == is_available)
            count_query = count_query.where(ProductVariant.is_available == is_available)

        total = await self.session.scalar(count_query)
        result = await self.session.execute(
            query.order_by(ProductVariant.display_order.asc(), ProductVariant.variant_name.asc()).offset(offset).limit(limit)
        )
        return result.scalars().all(), int(total or 0)

    async def list_selected(self, product_id: UUID, selected_variants: dict[str, str]) -> Sequence[ProductVariant]:
        if not selected_variants:
            return []
        filters = [
            (ProductVariant.variant_type == variant_type) & (ProductVariant.variant_value == variant_value)
            for variant_type, variant_value in selected_variants.items()
        ]
        result = await self.session.execute(
            select(ProductVariant).where(
                ProductVariant.product_id == product_id,
                ProductVariant.is_available.is_(True),
                or_(*filters),
            )
        )
        return result.scalars().all()
