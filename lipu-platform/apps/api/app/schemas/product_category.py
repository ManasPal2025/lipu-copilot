"""Product category schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import Field, field_validator

from app.schemas.base import APIModel


class ProductCategoryBase(APIModel):
    organization_id: UUID
    name: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: str | None = None
    parent_category_id: UUID | None = None
    icon_url: str | None = Field(default=None, max_length=500)
    display_order: int = 0
    is_active: bool = True
    seo_title: str | None = Field(default=None, max_length=255)
    seo_description: str | None = Field(default=None, max_length=500)
    seo_keywords: str | None = Field(default=None, max_length=500)

    @field_validator("name", "slug")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty.")
        return value


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategoryUpdate(APIModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    slug: str | None = Field(default=None, min_length=2, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: str | None = None
    parent_category_id: UUID | None = None
    icon_url: str | None = Field(default=None, max_length=500)
    display_order: int | None = None
    is_active: bool | None = None
    seo_title: str | None = Field(default=None, max_length=255)
    seo_description: str | None = Field(default=None, max_length=500)
    seo_keywords: str | None = Field(default=None, max_length=500)

    @field_validator("name", "slug")
    @classmethod
    def strip_optional_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty.")
        return value


class ProductCategoryRead(ProductCategoryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

