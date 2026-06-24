"""Pydantic schema package."""

from app.schemas.organization import OrganizationCreate, OrganizationRead, OrganizationUpdate
from app.schemas.pagination import Page
from app.schemas.product import ProductCreate, ProductDetailRead, ProductRead, ProductUpdate
from app.schemas.product_category import ProductCategoryCreate, ProductCategoryRead, ProductCategoryUpdate
from app.schemas.product_variant import ProductVariantCreate, ProductVariantCreateForProduct, ProductVariantRead, ProductVariantUpdate
from app.schemas.quote import (
    QuoteConvertToOrder,
    QuoteCreate,
    QuoteDetailRead,
    QuoteItemCreate,
    QuoteItemRead,
    QuoteItemUpdate,
    QuoteRead,
    QuoteReject,
    QuoteUpdate,
)
from app.schemas.user import UserCreate, UserRead, UserUpdate

__all__ = [
    "OrganizationCreate",
    "OrganizationRead",
    "OrganizationUpdate",
    "Page",
    "ProductCategoryCreate",
    "ProductCategoryRead",
    "ProductCategoryUpdate",
    "ProductCreate",
    "ProductDetailRead",
    "ProductRead",
    "ProductUpdate",
    "ProductVariantCreate",
    "ProductVariantCreateForProduct",
    "ProductVariantRead",
    "ProductVariantUpdate",
    "QuoteConvertToOrder",
    "QuoteCreate",
    "QuoteDetailRead",
    "QuoteItemCreate",
    "QuoteItemRead",
    "QuoteItemUpdate",
    "QuoteRead",
    "QuoteReject",
    "QuoteUpdate",
    "UserCreate",
    "UserRead",
    "UserUpdate",
]
