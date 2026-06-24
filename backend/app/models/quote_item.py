"""Quote item ORM model."""

from decimal import Decimal
from uuid import UUID as PythonUUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, Numeric
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class QuoteItem(BaseModel):
    """Line item for a quote."""

    __tablename__ = "quote_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_quote_items_quantity_positive"),
        Index("idx_quote_items_quote", "quote_id"),
        Index("idx_quote_items_product", "product_id"),
    )

    quote_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("quotes.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    selected_variants: Mapped[dict[str, str]] = mapped_column(JSONB, nullable=False)
    custom_width: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    custom_height: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    custom_depth: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    quote: Mapped["Quote"] = relationship(back_populates="items")

