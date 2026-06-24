"""Product catalog application service."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError, NotFoundError
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.product_variant import ProductVariant
from app.repositories.organization import OrganizationRepository
from app.repositories.product import ProductRepository
from app.repositories.product_category import ProductCategoryRepository
from app.repositories.product_variant import ProductVariantRepository
from app.schemas.pagination import Page
from app.schemas.product import ProductCreate, ProductRead, ProductSort, ProductUpdate
from app.schemas.product_category import ProductCategoryCreate, ProductCategoryRead, ProductCategoryUpdate
from app.schemas.product_variant import ProductVariantCreate, ProductVariantRead, ProductVariantUpdate
from app.services.base import BaseService


class ProductCatalogService(BaseService):
    """Use-case service for categories, products, and variants."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.organizations = OrganizationRepository(session)
        self.categories = ProductCategoryRepository(session)
        self.products = ProductRepository(session)
        self.variants = ProductVariantRepository(session)

    async def list_categories(
        self,
        *,
        organization_id: UUID | None = None,
        parent_category_id: UUID | None = None,
        is_active: bool | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> Page[ProductCategoryRead]:
        items, total = await self.categories.list_categories(
            organization_id=organization_id,
            parent_category_id=parent_category_id,
            is_active=is_active,
            offset=offset,
            limit=limit,
        )
        return Page[ProductCategoryRead](items=list(items), total=total, offset=offset, limit=limit)

    async def get_category(self, category_id: UUID) -> ProductCategory:
        category = await self.categories.get_active(category_id)
        if category is None:
            raise NotFoundError("Product category not found.")
        return category

    async def create_category(self, payload: ProductCategoryCreate) -> ProductCategory:
        await self._ensure_organization_exists(payload.organization_id)
        if payload.parent_category_id is not None:
            parent = await self.get_category(payload.parent_category_id)
            if parent.organization_id != payload.organization_id:
                raise ConflictError("Parent category belongs to a different organization.")

        if await self.categories.get_by_slug(payload.organization_id, payload.slug):
            raise ConflictError("Product category slug already exists.", details={"slug": payload.slug})

        category = await self.categories.create(**payload.model_dump())
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def update_category(self, category_id: UUID, payload: ProductCategoryUpdate) -> ProductCategory:
        category = await self.get_category(category_id)
        values = payload.model_dump(exclude_unset=True)

        if values.get("parent_category_id") == category_id:
            raise ConflictError("A category cannot be its own parent.")
        if values.get("parent_category_id") is not None:
            parent = await self.get_category(values["parent_category_id"])
            if parent.organization_id != category.organization_id:
                raise ConflictError("Parent category belongs to a different organization.")

        if "slug" in values:
            existing = await self.categories.get_by_slug(category.organization_id, values["slug"])
            if existing and existing.id != category_id:
                raise ConflictError("Product category slug already exists.", details={"slug": values["slug"]})

        updated = await self.categories.update(category, **values)
        await self.session.commit()
        await self.session.refresh(updated)
        return updated

    async def delete_category(self, category_id: UUID) -> None:
        category = await self.get_category(category_id)
        if await self.products.count_by_category(category_id):
            raise ConflictError("Cannot delete a category that still has products.")
        await self.categories.delete(category)
        await self.session.commit()

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
        sort: ProductSort = "-created_at",
        offset: int = 0,
        limit: int = 100,
    ) -> Page[ProductRead]:
        if min_price is not None and max_price is not None and min_price > max_price:
            raise BadRequestError("min_price cannot be greater than max_price.")

        items, total = await self.products.list_products(
            organization_id=organization_id,
            category_id=category_id,
            status=status,
            visibility=visibility,
            is_bestseller=is_bestseller,
            min_price=min_price,
            max_price=max_price,
            search=search,
            sort=sort,
            offset=offset,
            limit=limit,
        )
        return Page[ProductRead](items=list(items), total=total, offset=offset, limit=limit)

    async def get_product(self, product_id: UUID, *, include_variants: bool = True) -> Product:
        product = await self.products.get_active(product_id, include_variants=include_variants)
        if product is None:
            raise NotFoundError("Product not found.")
        return product

    async def create_product(self, payload: ProductCreate) -> Product:
        await self._ensure_organization_exists(payload.organization_id)
        category = await self.get_category(payload.category_id)
        if category.organization_id != payload.organization_id:
            raise ConflictError("Product category belongs to a different organization.")

        if await self.products.get_by_slug(payload.organization_id, payload.slug):
            raise ConflictError("Product slug already exists.", details={"slug": payload.slug})
        if await self.products.get_by_sku(payload.organization_id, payload.sku):
            raise ConflictError("Product SKU already exists.", details={"sku": payload.sku})

        product = await self.products.create(**self._to_model_values(payload.model_dump()))
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update_product(self, product_id: UUID, payload: ProductUpdate) -> Product:
        product = await self.get_product(product_id, include_variants=False)
        values = self._to_model_values(payload.model_dump(exclude_unset=True))

        if "category_id" in values:
            category = await self.get_category(values["category_id"])
            if category.organization_id != product.organization_id:
                raise ConflictError("Product category belongs to a different organization.")

        if "slug" in values:
            existing = await self.products.get_by_slug(product.organization_id, values["slug"])
            if existing and existing.id != product_id:
                raise ConflictError("Product slug already exists.", details={"slug": values["slug"]})
        if "sku" in values:
            existing = await self.products.get_by_sku(product.organization_id, values["sku"])
            if existing and existing.id != product_id:
                raise ConflictError("Product SKU already exists.", details={"sku": values["sku"]})

        updated = await self.products.update(product, **values)
        await self.session.commit()
        await self.session.refresh(updated)
        return updated

    async def delete_product(self, product_id: UUID) -> None:
        product = await self.get_product(product_id, include_variants=False)
        product.deleted_at = datetime.now(UTC)
        await self.session.commit()

    async def list_variants(
        self,
        *,
        product_id: UUID,
        variant_type: str | None = None,
        is_available: bool | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> Page[ProductVariantRead]:
        await self.get_product(product_id, include_variants=False)
        items, total = await self.variants.list_variants(
            product_id=product_id,
            variant_type=variant_type,
            is_available=is_available,
            offset=offset,
            limit=limit,
        )
        return Page[ProductVariantRead](items=list(items), total=total, offset=offset, limit=limit)

    async def get_variant(self, variant_id: UUID) -> ProductVariant:
        variant = await self.variants.get_by_id(variant_id)
        if variant is None:
            raise NotFoundError("Product variant not found.")
        return variant

    async def create_variant(self, payload: ProductVariantCreate) -> ProductVariant:
        await self.get_product(payload.product_id, include_variants=False)
        if await self.variants.get_by_value(payload.product_id, payload.variant_type, payload.variant_value):
            raise ConflictError(
                "Product variant value already exists.",
                details={"variant_type": payload.variant_type, "variant_value": payload.variant_value},
            )

        variant = await self.variants.create(**self._to_model_values(payload.model_dump()))
        await self.session.commit()
        await self.session.refresh(variant)
        return variant

    async def update_variant(self, variant_id: UUID, payload: ProductVariantUpdate) -> ProductVariant:
        variant = await self.get_variant(variant_id)
        values = self._to_model_values(payload.model_dump(exclude_unset=True))
        variant_type = values.get("variant_type", variant.variant_type)
        variant_value = values.get("variant_value", variant.variant_value)

        if "variant_type" in values or "variant_value" in values:
            existing = await self.variants.get_by_value(variant.product_id, variant_type, variant_value)
            if existing and existing.id != variant_id:
                raise ConflictError(
                    "Product variant value already exists.",
                    details={"variant_type": variant_type, "variant_value": variant_value},
                )

        updated = await self.variants.update(variant, **values)
        await self.session.commit()
        await self.session.refresh(updated)
        return updated

    async def delete_variant(self, variant_id: UUID) -> None:
        variant = await self.get_variant(variant_id)
        await self.variants.delete(variant)
        await self.session.commit()

    async def _ensure_organization_exists(self, organization_id: UUID) -> None:
        organization = await self.organizations.get_active(organization_id)
        if organization is None:
            raise NotFoundError("Organization not found.", details={"organization_id": str(organization_id)})

    def _to_model_values(self, values: dict[str, Any]) -> dict[str, Any]:
        if "metadata" in values:
            values["metadata_"] = values.pop("metadata")
        return values
