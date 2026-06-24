"""Product ORM model."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any
from uuid import UUID as PythonUUID

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.product_category import ProductCategory
    from app.models.product_variant import ProductVariant


class Product(BaseModel):
    """Product catalog item."""

    __tablename__ = "products"
    __table_args__ = (
        UniqueConstraint("organization_id", "sku", name="uq_products_organization_id_sku"),
        UniqueConstraint("organization_id", "slug", name="uq_products_organization_id_slug"),
        Index("idx_products_category", "category_id"),
        Index("idx_products_status_visibility", "status", "visibility"),
        Index("idx_products_org_status", "organization_id", "status", "visibility"),
        Index("idx_products_search", "search_text", postgresql_using="gin"),
    )

    organization_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_categories.id", ondelete="RESTRICT"),
        nullable=False,
    )
    sku: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    long_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    short_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    base_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    installation_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, server_default="0", nullable=False)
    discount_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0, server_default="0", nullable=False)
    cost_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    default_width: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    default_height: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    default_depth: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    weight_per_unit: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    unit_of_measure: Mapped[str] = mapped_column(String(20), default="piece", server_default="piece", nullable=False)
    featured_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    gallery_images: Mapped[list[str]] = mapped_column(JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False)
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    brochure_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    seo_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    seo_keywords: Mapped[str | None] = mapped_column(String(500), nullable=True)
    search_text: Mapped[Any | None] = mapped_column(TSVECTOR, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active", nullable=False)
    visibility: Mapped[str] = mapped_column(String(50), default="public", server_default="public", nullable=False)
    warranty_months: Mapped[int] = mapped_column(Integer, default=60, server_default="60", nullable=False)
    is_bestseller: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    specifications: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    organization: Mapped["Organization"] = relationship()
    category: Mapped["ProductCategory"] = relationship(back_populates="products")
    variants: Mapped[list["ProductVariant"]] = relationship(back_populates="product", cascade="all, delete-orphan")

