"""Quote management service."""

from datetime import UTC, date, datetime
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError, NotFoundError
from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.repositories.organization import OrganizationRepository
from app.repositories.product import ProductRepository
from app.repositories.product_variant import ProductVariantRepository
from app.repositories.quote import QuoteRepository
from app.repositories.quote_item import QuoteItemRepository
from app.repositories.user import UserRepository
from app.schemas.pagination import Page
from app.schemas.quote import (
    QuoteConvertToOrder,
    QuoteCreate,
    QuoteItemCreate,
    QuoteItemUpdate,
    QuoteRead,
    QuoteReject,
    QuoteSort,
    QuoteStatus,
    QuoteUpdate,
)
from app.services.base import BaseService


MONEY = Decimal("0.01")


class QuoteService(BaseService):
    """Use-case service for quote workflows and calculations."""

    EDITABLE_STATUSES = {"draft"}
    EXPIRABLE_STATUSES = {"draft", "sent"}

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.organizations = OrganizationRepository(session)
        self.users = UserRepository(session)
        self.products = ProductRepository(session)
        self.variants = ProductVariantRepository(session)
        self.quotes = QuoteRepository(session)
        self.items = QuoteItemRepository(session)

    async def list_quotes(
        self,
        *,
        organization_id: UUID | None = None,
        customer_id: UUID | None = None,
        status: QuoteStatus | None = None,
        valid_from: date | None = None,
        valid_to: date | None = None,
        sort: QuoteSort = "-created_at",
        offset: int = 0,
        limit: int = 100,
    ) -> Page[QuoteRead]:
        if valid_from and valid_to and valid_from > valid_to:
            raise BadRequestError("valid_from cannot be after valid_to.")
        rows, total = await self.quotes.list_quotes(
            organization_id=organization_id,
            customer_id=customer_id,
            status=status,
            valid_from=valid_from,
            valid_to=valid_to,
            sort=sort,
            offset=offset,
            limit=limit,
        )
        return Page[QuoteRead](items=list(rows), total=total, offset=offset, limit=limit)

    async def get_quote(self, quote_id: UUID, *, include_items: bool = True) -> Quote:
        quote = await self.quotes.get_active(quote_id, include_items=include_items)
        if quote is None:
            raise NotFoundError("Quote not found.")
        await self._expire_if_needed(quote)
        return quote

    async def create_quote(self, payload: QuoteCreate) -> Quote:
        await self._validate_customer(payload.organization_id, payload.customer_id)
        values = self._to_model_values(payload.model_dump(exclude={"items"}))
        values["quote_number"] = values.get("quote_number") or await self._generate_quote_number()
        if await self.quotes.get_by_number(values["quote_number"]):
            raise ConflictError("Quote number already exists.", details={"quote_number": values["quote_number"]})

        quote = await self.quotes.create(**values)
        for item_payload in payload.items:
            item_values = await self._build_item_values(quote, item_payload)
            await self.items.create(**item_values)

        await self._recalculate_quote(quote)
        await self.session.commit()
        return await self.get_quote(quote.id, include_items=True)

    async def update_quote(self, quote_id: UUID, payload: QuoteUpdate) -> Quote:
        quote = await self.get_quote(quote_id, include_items=False)
        self._ensure_editable(quote)
        values = self._to_model_values(payload.model_dump(exclude_unset=True))
        for numeric_key in ("discount_percentage", "discount_amount", "tax_rate"):
            if numeric_key in values and values[numeric_key] is None:
                raise BadRequestError(f"{numeric_key} cannot be null.")
        discount_percentage = values.get("discount_percentage", Decimal("0"))
        discount_amount = values.get("discount_amount", Decimal("0"))
        if discount_percentage > 0 and "discount_amount" not in values:
            values["discount_amount"] = Decimal("0")
        if discount_amount > 0 and "discount_percentage" not in values:
            values["discount_percentage"] = Decimal("0")
        for key, value in values.items():
            setattr(quote, key, value)
        await self._recalculate_quote(quote)
        await self.session.commit()
        return await self.get_quote(quote_id, include_items=True)

    async def delete_quote(self, quote_id: UUID) -> None:
        quote = await self.get_quote(quote_id, include_items=False)
        if quote.status not in {"draft", "rejected", "expired"}:
            raise ConflictError("Only draft, rejected, or expired quotes can be deleted.")
        quote.deleted_at = datetime.now(UTC)
        await self.session.commit()

    async def add_item(self, quote_id: UUID, payload: QuoteItemCreate) -> QuoteItem:
        quote = await self.get_quote(quote_id, include_items=False)
        self._ensure_editable(quote)
        item = await self.items.create(**await self._build_item_values(quote, payload))
        await self._recalculate_quote(quote)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def update_item(self, quote_id: UUID, item_id: UUID, payload: QuoteItemUpdate) -> QuoteItem:
        quote = await self.get_quote(quote_id, include_items=False)
        self._ensure_editable(quote)
        item = await self.items.get_for_quote(quote_id, item_id)
        if item is None:
            raise NotFoundError("Quote item not found.")

        values = payload.model_dump(exclude_unset=True)
        if "quantity" in values:
            item.quantity = values["quantity"]
        if "selected_variants" in values:
            item.selected_variants = values["selected_variants"]
        for key in ("custom_width", "custom_height", "custom_depth"):
            if key in values:
                setattr(item, key, values[key])

        if "unit_price_override" in values or "selected_variants" in values:
            product = await self._get_quote_product(quote, item.product_id)
            unit_price = values.get("unit_price_override")
            if unit_price is None:
                unit_price = await self._calculate_product_unit_price(product.id, product.base_price, item.selected_variants)
            item.unit_price = self._money(unit_price)

        item.total_price = self._money(item.unit_price * item.quantity)
        await self._recalculate_quote(quote)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete_item(self, quote_id: UUID, item_id: UUID) -> None:
        quote = await self.get_quote(quote_id, include_items=False)
        self._ensure_editable(quote)
        item = await self.items.get_for_quote(quote_id, item_id)
        if item is None:
            raise NotFoundError("Quote item not found.")
        await self.items.delete(item)
        await self._recalculate_quote(quote)
        await self.session.commit()

    async def send_quote(self, quote_id: UUID) -> Quote:
        quote = await self.get_quote(quote_id, include_items=False)
        self._ensure_status(quote, {"draft"})
        if quote.valid_until and quote.valid_until < datetime.now(UTC).date():
            quote.status = "expired"
            await self.session.commit()
            raise ConflictError("Expired quotes cannot be sent.")
        if not await self.items.list_for_quote(quote_id):
            raise ConflictError("A quote must contain at least one item before it can be sent.")
        quote.status = "sent"
        quote.sent_date = datetime.now(UTC)
        await self.session.commit()
        return await self.get_quote(quote_id, include_items=True)

    async def accept_quote(self, quote_id: UUID) -> Quote:
        quote = await self.get_quote(quote_id, include_items=False)
        self._ensure_status(quote, {"sent"})
        quote.status = "accepted"
        quote.accepted_date = datetime.now(UTC)
        await self.session.commit()
        return await self.get_quote(quote_id, include_items=True)

    async def reject_quote(self, quote_id: UUID, payload: QuoteReject) -> Quote:
        quote = await self.get_quote(quote_id, include_items=False)
        self._ensure_status(quote, {"sent"})
        quote.status = "rejected"
        quote.rejected_date = datetime.now(UTC)
        if payload.reason:
            metadata = dict(quote.metadata_ or {})
            metadata["rejection_reason"] = payload.reason
            quote.metadata_ = metadata
        await self.session.commit()
        return await self.get_quote(quote_id, include_items=True)

    async def convert_to_order(self, quote_id: UUID, payload: QuoteConvertToOrder) -> Quote:
        quote = await self.get_quote(quote_id, include_items=False)
        self._ensure_status(quote, {"accepted"})
        quote.status = "converted_to_order"
        quote.converted_to_order_id = payload.order_id
        await self.session.commit()
        return await self.get_quote(quote_id, include_items=True)

    async def _build_item_values(self, quote: Quote, payload: QuoteItemCreate) -> dict[str, object]:
        product = await self._get_quote_product(quote, payload.product_id)
        unit_price = payload.unit_price_override
        if unit_price is None:
            unit_price = await self._calculate_product_unit_price(product.id, product.base_price, payload.selected_variants)
        unit_price = self._money(unit_price)
        return {
            "quote_id": quote.id,
            "product_id": payload.product_id,
            "quantity": payload.quantity,
            "unit_price": unit_price,
            "total_price": self._money(unit_price * payload.quantity),
            "selected_variants": payload.selected_variants,
            "custom_width": payload.custom_width,
            "custom_height": payload.custom_height,
            "custom_depth": payload.custom_depth,
        }

    async def _get_quote_product(self, quote: Quote, product_id: UUID):
        product = await self.products.get_active(product_id, include_variants=False)
        if product is None:
            raise NotFoundError("Product not found.", details={"product_id": str(product_id)})
        if product.organization_id != quote.organization_id:
            raise ConflictError("Product belongs to a different organization.")
        if product.status != "active":
            raise ConflictError("Only active products can be added to a quote.")
        return product

    async def _calculate_product_unit_price(
        self,
        product_id: UUID,
        base_price: Decimal,
        selected_variants: dict[str, str],
    ) -> Decimal:
        selected = await self.variants.list_selected(product_id, selected_variants)
        if len(selected) != len(selected_variants):
            raise ConflictError("One or more selected variants are unavailable for this product.")
        return base_price + sum((variant.price_modifier for variant in selected), Decimal("0"))

    async def _recalculate_quote(self, quote: Quote) -> None:
        items = await self.items.list_for_quote(quote.id)
        subtotal = self._money(sum((item.total_price for item in items), Decimal("0")))
        quote.subtotal = subtotal
        if quote.discount_percentage > 0:
            discount = self._money(subtotal * quote.discount_percentage / Decimal("100"))
            quote.discount_amount = discount
        else:
            discount = self._money(quote.discount_amount)
        if discount > subtotal:
            raise BadRequestError("Discount amount cannot exceed quote subtotal.")
        taxable_base = subtotal - discount
        quote.tax_amount = self._money(taxable_base * quote.tax_rate / Decimal("100"))
        quote.total_amount = self._money(taxable_base + quote.tax_amount)

    async def _validate_customer(self, organization_id: UUID, customer_id: UUID) -> None:
        organization = await self.organizations.get_active(organization_id)
        if organization is None:
            raise NotFoundError("Organization not found.", details={"organization_id": str(organization_id)})
        customer = await self.users.get_active(customer_id)
        if customer is None:
            raise NotFoundError("Customer not found.", details={"customer_id": str(customer_id)})
        if customer.organization_id != organization_id:
            raise ConflictError("Customer belongs to a different organization.")

    async def _generate_quote_number(self) -> str:
        for _ in range(5):
            candidate = f"Q-{datetime.now(UTC):%Y%m%d}-{uuid4().hex[:8].upper()}"
            if not await self.quotes.get_by_number(candidate):
                return candidate
        raise ConflictError("Could not generate a unique quote number.")

    async def _expire_if_needed(self, quote: Quote) -> None:
        if quote.status in self.EXPIRABLE_STATUSES and quote.valid_until and quote.valid_until < datetime.now(UTC).date():
            quote.status = "expired"
            await self.session.commit()
            await self.session.refresh(quote)

    def _ensure_editable(self, quote: Quote) -> None:
        self._ensure_status(quote, self.EDITABLE_STATUSES, message="Only draft quotes can be edited.")

    def _ensure_status(self, quote: Quote, allowed: set[str], message: str | None = None) -> None:
        if quote.status not in allowed:
            raise ConflictError(message or f"Quote status '{quote.status}' does not allow this action.")

    def _to_model_values(self, values: dict[str, object]) -> dict[str, object]:
        if "metadata" in values:
            values["metadata_"] = values.pop("metadata")
        return values

    def _money(self, value: Decimal) -> Decimal:
        return value.quantize(MONEY, rounding=ROUND_HALF_UP)
