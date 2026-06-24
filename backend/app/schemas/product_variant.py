"""Product variant schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import AliasChoices, Field, field_validator

from app.schemas.base import APIModel


class ProductVariantBase(APIModel):
    product_id: UUID
    variant_type: str = Field(min_length=2, max_length=50)
    variant_name: str = Field(min_length=1, max_length=255)
    variant_value: str = Field(min_length=1, max_length=255)
    price_modifier: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=2)
    image_url: str | None = Field(default=None, max_length=500)
    color_hex: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    stock_quantity: int = Field(default=0, ge=0)
    is_available: bool = True
    display_order: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict, validation_alias=AliasChoices("metadata_", "metadata"))

    @field_validator("variant_type", "variant_name", "variant_value")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty.")
        return value


class ProductVariantCreate(ProductVariantBase):
    pass


class ProductVariantCreateForProduct(APIModel):
    variant_type: str = Field(min_length=2, max_length=50)
    variant_name: str = Field(min_length=1, max_length=255)
    variant_value: str = Field(min_length=1, max_length=255)
    price_modifier: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=2)
    image_url: str | None = Field(default=None, max_length=500)
    color_hex: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    stock_quantity: int = Field(default=0, ge=0)
    is_available: bool = True
    display_order: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict, validation_alias=AliasChoices("metadata_", "metadata"))


class ProductVariantUpdate(APIModel):
    variant_type: str | None = Field(default=None, min_length=2, max_length=50)
    variant_name: str | None = Field(default=None, min_length=1, max_length=255)
    variant_value: str | None = Field(default=None, min_length=1, max_length=255)
    price_modifier: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    image_url: str | None = Field(default=None, max_length=500)
    color_hex: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    stock_quantity: int | None = Field(default=None, ge=0)
    is_available: bool | None = None
    display_order: int | None = None
    metadata: dict[str, Any] | None = Field(default=None, validation_alias=AliasChoices("metadata_", "metadata"))


class ProductVariantRead(ProductVariantBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
