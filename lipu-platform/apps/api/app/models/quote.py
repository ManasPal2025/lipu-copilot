"""Quote ORM model."""

from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Any
from uuid import UUID as PythonUUID

from sqlalchemy import Date, DateTime, ForeignKey, Index, Numeric, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.quote_item import QuoteItem
    from app.models.user import User


class Quote(BaseModel):
    """Customer quote with pricing totals and workflow state."""

    __tablename__ = "quotes"
    __table_args__ = (
        UniqueConstraint("quote_number", name="uq_quotes_quote_number"),
        Index("idx_quotes_customer", "customer_id"),
        Index("idx_quotes_status", "status"),
        Index("idx_quotes_number", "quote_number"),
        Index("idx_quotes_valid_until", "valid_until"),
        Index("idx_quotes_organization_status", "organization_id", "status"),
    )

    organization_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    customer_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    quote_number: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, server_default="0", nullable=False)
    discount_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0, server_default="0", nullable=False)
    discount_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, server_default="0", nullable=False)
    tax_rate: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0, server_default="0", nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, server_default="0", nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0, server_default="0", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", server_default="draft", nullable=False)
    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    sent_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    valid_until: Mapped[date | None] = mapped_column(Date, nullable=True)
    accepted_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejected_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    terms_and_conditions: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    converted_to_order_id: Mapped[PythonUUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    metadata_: Mapped[dict[str, Any]] = mapped_column("metadata", JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    organization: Mapped["Organization"] = relationship()
    customer: Mapped["User"] = relationship()
    items: Mapped[list["QuoteItem"]] = relationship(back_populates="quote", cascade="all, delete-orphan")
