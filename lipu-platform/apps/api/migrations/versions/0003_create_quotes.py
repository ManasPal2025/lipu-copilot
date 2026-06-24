"""create quotes

Revision ID: 0003_create_quotes
Revises: 0002_create_product_catalog
Create Date: 2026-06-24
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0003_create_quotes"
down_revision: str | None = "0002_create_product_catalog"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "quotes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quote_number", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("subtotal", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("discount_percentage", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("discount_amount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("tax_rate", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("tax_amount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("total_amount", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="draft"),
        sa.Column("created_date", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("sent_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("valid_until", sa.Date(), nullable=True),
        sa.Column("accepted_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejected_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("terms_and_conditions", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("converted_to_order_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "subtotal >= 0 AND discount_percentage >= 0 AND discount_amount >= 0 AND tax_rate >= 0 AND tax_amount >= 0 AND total_amount >= 0",
            name="ck_quotes_non_negative_amounts",
        ),
        sa.CheckConstraint(
            "status IN ('draft', 'sent', 'accepted', 'rejected', 'expired', 'converted_to_order')",
            name="ck_quotes_status",
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_quotes_organization_id_organizations",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(["customer_id"], ["users.id"], name="fk_quotes_customer_id_users"),
        sa.PrimaryKeyConstraint("id", name="pk_quotes"),
        sa.UniqueConstraint("quote_number", name="uq_quotes_quote_number"),
    )
    op.create_index("idx_quotes_customer", "quotes", ["customer_id"])
    op.create_index("idx_quotes_status", "quotes", ["status"])
    op.create_index("idx_quotes_number", "quotes", ["quote_number"])
    op.create_index(
        "idx_quotes_valid_until",
        "quotes",
        ["valid_until"],
        postgresql_where=sa.text("status IN ('sent', 'draft')"),
    )
    op.create_index("idx_quotes_organization_status", "quotes", ["organization_id", "status"])

    op.create_table(
        "quote_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("quote_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("unit_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("selected_variants", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("custom_width", sa.Numeric(10, 2), nullable=True),
        sa.Column("custom_height", sa.Numeric(10, 2), nullable=True),
        sa.Column("custom_depth", sa.Numeric(10, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint("quantity > 0", name="ck_quote_items_quantity_positive"),
        sa.CheckConstraint("unit_price >= 0 AND total_price >= 0", name="ck_quote_items_non_negative_amounts"),
        sa.ForeignKeyConstraint(["quote_id"], ["quotes.id"], name="fk_quote_items_quote_id_quotes", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], name="fk_quote_items_product_id_products"),
        sa.PrimaryKeyConstraint("id", name="pk_quote_items"),
    )
    op.create_index("idx_quote_items_quote", "quote_items", ["quote_id"])
    op.create_index("idx_quote_items_product", "quote_items", ["product_id"])


def downgrade() -> None:
    op.drop_index("idx_quote_items_product", table_name="quote_items")
    op.drop_index("idx_quote_items_quote", table_name="quote_items")
    op.drop_table("quote_items")
    op.drop_index("idx_quotes_organization_status", table_name="quotes")
    op.drop_index("idx_quotes_valid_until", table_name="quotes")
    op.drop_index("idx_quotes_number", table_name="quotes")
    op.drop_index("idx_quotes_status", table_name="quotes")
    op.drop_index("idx_quotes_customer", table_name="quotes")
    op.drop_table("quotes")

