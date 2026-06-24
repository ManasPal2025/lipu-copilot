"""Quote request and response schemas."""

from datetime import UTC, date, datetime
from decimal import Decimal
from typing import Any, Literal
from uuid import UUID

from pydantic import AliasChoices, Field, field_validator, model_validator

from app.schemas.base import APIModel


QuoteStatus = Literal["draft", "sent", "accepted", "rejected", "expired", "converted_to_order"]
QuoteSort = Literal["created_at", "-created_at", "valid_until", "-valid_until", "total_amount", "-total_amount"]


class QuoteItemBase(APIModel):
    product_id: UUID
    quantity: int = Field(gt=0)
    selected_variants: dict[str, str] = Field(default_factory=dict)
    custom_width: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    custom_height: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    custom_depth: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    unit_price_override: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)


class QuoteItemCreate(QuoteItemBase):
    pass


class QuoteItemUpdate(APIModel):
    quantity: int | None = Field(default=None, gt=0)
    selected_variants: dict[str, str] | None = None
    custom_width: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    custom_height: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    custom_depth: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    unit_price_override: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)


class QuoteItemRead(APIModel):
    id: UUID
    quote_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal
    total_price: Decimal
    selected_variants: dict[str, str]
    custom_width: Decimal | None = None
    custom_height: Decimal | None = None
    custom_depth: Decimal | None = None
    created_at: datetime
    updated_at: datetime


class QuoteBase(APIModel):
    organization_id: UUID
    customer_id: UUID
    title: str = Field(min_length=2, max_length=255)
    description: str | None = None
    valid_until: date | None = None
    terms_and_conditions: str | None = None
    notes: str | None = None
    discount_percentage: Decimal = Field(default=Decimal("0"), ge=0, le=100, max_digits=5, decimal_places=2)
    discount_amount: Decimal = Field(default=Decimal("0"), ge=0, max_digits=12, decimal_places=2)
    tax_rate: Decimal = Field(default=Decimal("0"), ge=0, le=100, max_digits=5, decimal_places=2)
    metadata: dict[str, Any] = Field(default_factory=dict, validation_alias=AliasChoices("metadata_", "metadata"))

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty.")
        return value

    @field_validator("valid_until")
    @classmethod
    def validate_valid_until(cls, value: date | None) -> date | None:
        if value is not None and value < datetime.now(UTC).date():
            raise ValueError("valid_until cannot be in the past.")
        return value

    @model_validator(mode="after")
    def validate_discount_mode(self) -> "QuoteBase":
        if self.discount_percentage > 0 and self.discount_amount > 0:
            raise ValueError("Use either discount_percentage or discount_amount, not both.")
        return self


class QuoteCreate(QuoteBase):
    quote_number: str | None = Field(default=None, min_length=3, max_length=50)
    items: list[QuoteItemCreate] = Field(default_factory=list)


class QuoteUpdate(APIModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    description: str | None = None
    valid_until: date | None = None
    terms_and_conditions: str | None = None
    notes: str | None = None
    discount_percentage: Decimal | None = Field(default=None, ge=0, le=100, max_digits=5, decimal_places=2)
    discount_amount: Decimal | None = Field(default=None, ge=0, max_digits=12, decimal_places=2)
    tax_rate: Decimal | None = Field(default=None, ge=0, le=100, max_digits=5, decimal_places=2)
    metadata: dict[str, Any] | None = Field(default=None, validation_alias=AliasChoices("metadata_", "metadata"))

    @field_validator("valid_until")
    @classmethod
    def validate_valid_until(cls, value: date | None) -> date | None:
        if value is not None and value < datetime.now(UTC).date():
            raise ValueError("valid_until cannot be in the past.")
        return value

    @model_validator(mode="after")
    def validate_discount_mode(self) -> "QuoteUpdate":
        if self.discount_percentage and self.discount_percentage > 0 and self.discount_amount and self.discount_amount > 0:
            raise ValueError("Use either discount_percentage or discount_amount, not both.")
        return self


class QuoteRead(APIModel):
    id: UUID
    organization_id: UUID
    customer_id: UUID
    quote_number: str
    title: str
    description: str | None = None
    subtotal: Decimal
    discount_percentage: Decimal
    discount_amount: Decimal
    tax_rate: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    status: QuoteStatus
    created_date: datetime
    sent_date: datetime | None = None
    valid_until: date | None = None
    accepted_date: datetime | None = None
    rejected_date: datetime | None = None
    terms_and_conditions: str | None = None
    notes: str | None = None
    converted_to_order_id: UUID | None = None
    metadata: dict[str, Any] = Field(default_factory=dict, validation_alias=AliasChoices("metadata_", "metadata"))
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class QuoteDetailRead(QuoteRead):
    items: list[QuoteItemRead] = Field(default_factory=list)


class QuoteReject(APIModel):
    reason: str | None = Field(default=None, max_length=1000)


class QuoteConvertToOrder(APIModel):
    order_id: UUID
