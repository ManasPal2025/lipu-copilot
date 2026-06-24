"""Product schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

from pydantic import AliasChoices, Field, field_validator

from app.schemas.base import APIModel
from app.schemas.product_variant import ProductVariantRead


ProductStatus = Literal["active", "inactive", "discontinued"]
ProductVisibility = Literal["public", "private", "draft"]
ProductSort = Literal["created_at", "-created_at", "name", "-name", "base_price", "-base_price", "display_order", "-display_order"]


class ProductBase(APIModel):
    organization_id: UUID
    category_id: UUID
    sku: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: str | None = None
    long_description: str | None = None
    short_description: str | None = Field(default=None, max_length=500)
    base_price: Decimal = Field(ge=0, max_digits=12, decimal_places=2)
    installation_cost: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=2)
    discount_percentage: Decimal = Field(default=Decimal("0"), ge=0, le=100, max_digits=5, decimal_places=2)
    cost_price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    default_width: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    default_height: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    default_depth: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    weight_per_unit: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    unit_of_measure: str = Field(default="piece", max_length=20)
    featured_image_url: str | None = Field(default=None, max_length=500)
    gallery_images: list[str] = Field(default_factory=list)
    video_url: str | None = Field(default=None, max_length=500)
    brochure_url: str | None = Field(default=None, max_length=500)
    seo_title: str | None = Field(default=None, max_length=255)
    seo_description: str | None = Field(default=None, max_length=500)
    seo_keywords: str | None = Field(default=None, max_length=500)
    status: ProductStatus = "active"
    visibility: ProductVisibility = "public"
    warranty_months: int = Field(default=60, ge=0)
    is_bestseller: bool = False
    display_order: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict, validation_alias=AliasChoices("metadata_", "metadata"))
    specifications: dict[str, Any] = Field(default_factory=dict)

    @field_validator("sku", "name", "slug")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty.")
        return value


class ProductCreate(ProductBase):
    pass


class ProductUpdate(APIModel):
    category_id: UUID | None = None
    sku: str | None = Field(default=None, min_length=1, max_length=100)
    name: str | None = Field(default=None, min_length=2, max_length=255)
    slug: str | None = Field(default=None, min_length=2, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: str | None = None
    long_description: str | None = None
    short_description: str | None = Field(default=None, max_length=500)
    base_price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    installation_cost: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    discount_percentage: Decimal | None = Field(default=None, ge=0, le=100, max_digits=5, decimal_places=2)
    cost_price: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    default_width: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    default_height: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    default_depth: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    weight_per_unit: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    unit_of_measure: str | None = Field(default=None, max_length=20)
    featured_image_url: str | None = Field(default=None, max_length=500)
    gallery_images: list[str] | None = None
    video_url: str | None = Field(default=None, max_length=500)
    brochure_url: str | None = Field(default=None, max_length=500)
    seo_title: str | None = Field(default=None, max_length=255)
    seo_description: str | None = Field(default=None, max_length=500)
    seo_keywords: str | None = Field(default=None, max_length=500)
    status: ProductStatus | None = None
    visibility: ProductVisibility | None = None
    warranty_months: int | None = Field(default=None, ge=0)
    is_bestseller: bool | None = None
    display_order: int | None = None
    metadata: dict[str, Any] | None = Field(default=None, validation_alias=AliasChoices("metadata_", "metadata"))
    specifications: dict[str, Any] | None = None


class ProductRead(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class ProductDetailRead(ProductRead):
    variants: list[ProductVariantRead] = Field(default_factory=list)
