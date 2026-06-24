"""Product variant ORM model."""

from decimal import Decimal
from typing import TYPE_CHECKING, Any
from uuid import UUID as PythonUUID

from sqlalchemy import Boolean, ForeignKey, Index, Integer, Numeric, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.product import Product


class ProductVariant(BaseModel):
    """Product variant for colors, glass, hardware, and other options."""

    __tablename__ = "product_variants"
    __table_args__ = (
        UniqueConstraint("product_id", "variant_type", "variant_value", name="uq_product_variants_product_id_variant_type_variant_value"),
        Index("idx_product_variants_product", "product_id"),
        Index("idx_product_variants_type", "variant_type"),
        Index("idx_product_variants_availability", "product_id", "is_available"),
    )

    product_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    variant_type: Mapped[str] = mapped_column(String(50), nullable=False)
    variant_name: Mapped[str] = mapped_column(String(255), nullable=False)
    variant_value: Mapped[str] = mapped_column(String(255), nullable=False)
    price_modifier: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, server_default="0", nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    color_hex: Mapped[str | None] = mapped_column(String(7), nullable=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)

    product: Mapped["Product"] = relationship(back_populates="variants")

