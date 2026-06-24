"""create product catalog

Revision ID: 0002_create_product_catalog
Revises: 0001_create_organizations_and_users
Create Date: 2026-06-24
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0002_create_product_catalog"
down_revision: str | None = "0001_create_organizations_and_users"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "product_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("parent_category_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("icon_url", sa.String(length=500), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("seo_title", sa.String(length=255), nullable=True),
        sa.Column("seo_description", sa.String(length=500), nullable=True),
        sa.Column("seo_keywords", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], name="fk_product_categories_organization_id_organizations"),
        sa.ForeignKeyConstraint(
            ["parent_category_id"],
            ["product_categories.id"],
            name="fk_product_categories_parent_category_id_product_categories",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_product_categories"),
        sa.UniqueConstraint("organization_id", "slug", name="uq_product_categories_organization_id_slug"),
    )
    op.create_index("idx_product_categories_parent", "product_categories", ["parent_category_id"])
    op.create_index("idx_product_categories_active", "product_categories", ["is_active"])

    op.create_table(
        "products",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sku", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("long_description", sa.Text(), nullable=True),
        sa.Column("short_description", sa.String(length=500), nullable=True),
        sa.Column("base_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("installation_cost", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("discount_percentage", sa.Numeric(5, 2), nullable=False, server_default="0"),
        sa.Column("cost_price", sa.Numeric(12, 2), nullable=True),
        sa.Column("default_width", sa.Numeric(10, 2), nullable=True),
        sa.Column("default_height", sa.Numeric(10, 2), nullable=True),
        sa.Column("default_depth", sa.Numeric(10, 2), nullable=True),
        sa.Column("weight_per_unit", sa.Numeric(10, 2), nullable=True),
        sa.Column("unit_of_measure", sa.String(length=20), nullable=False, server_default="piece"),
        sa.Column("featured_image_url", sa.String(length=500), nullable=True),
        sa.Column("gallery_images", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("video_url", sa.String(length=500), nullable=True),
        sa.Column("brochure_url", sa.String(length=500), nullable=True),
        sa.Column("seo_title", sa.String(length=255), nullable=True),
        sa.Column("seo_description", sa.String(length=500), nullable=True),
        sa.Column("seo_keywords", sa.String(length=500), nullable=True),
        sa.Column("search_text", postgresql.TSVECTOR(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("visibility", sa.String(length=50), nullable=False, server_default="public"),
        sa.Column("warranty_months", sa.Integer(), nullable=False, server_default="60"),
        sa.Column("is_bestseller", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("specifications", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("base_price >= 0 AND installation_cost >= 0 AND discount_percentage >= 0", name="ck_products_non_negative_prices"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], name="fk_products_organization_id_organizations"),
        sa.ForeignKeyConstraint(["category_id"], ["product_categories.id"], name="fk_products_category_id_product_categories"),
        sa.PrimaryKeyConstraint("id", name="pk_products"),
        sa.UniqueConstraint("organization_id", "sku", name="uq_products_organization_id_sku"),
        sa.UniqueConstraint("organization_id", "slug", name="uq_products_organization_id_slug"),
    )
    op.create_index("idx_products_category", "products", ["category_id"])
    op.create_index("idx_products_status_visibility", "products", ["status", "visibility"])
    op.create_index("idx_products_org_status", "products", ["organization_id", "status", "visibility"])
    op.create_index("idx_products_search", "products", ["search_text"], postgresql_using="gin")

    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_product_search_text()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.search_text := to_tsvector('english',
                COALESCE(NEW.name, '') || ' ' ||
                COALESCE(NEW.sku, '') || ' ' ||
                COALESCE(NEW.description, '') || ' ' ||
                COALESCE(NEW.short_description, '') || ' ' ||
                COALESCE(NEW.seo_keywords, '')
            );
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_update_product_search_text
        BEFORE INSERT OR UPDATE ON products
        FOR EACH ROW
        EXECUTE FUNCTION update_product_search_text();
        """
    )

    op.create_table(
        "product_variants",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("variant_type", sa.String(length=50), nullable=False),
        sa.Column("variant_name", sa.String(length=255), nullable=False),
        sa.Column("variant_value", sa.String(length=255), nullable=False),
        sa.Column("price_modifier", sa.Numeric(12, 2), nullable=False, server_default="0"),
        sa.Column("image_url", sa.String(length=500), nullable=True),
        sa.Column("color_hex", sa.String(length=7), nullable=True),
        sa.Column("stock_quantity", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.CheckConstraint("price_modifier >= 0 AND stock_quantity >= 0", name="ck_product_variants_non_negative_values"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], name="fk_product_variants_product_id_products", ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name="pk_product_variants"),
        sa.UniqueConstraint("product_id", "variant_type", "variant_value", name="uq_product_variants_product_id_variant_type_variant_value"),
    )
    op.create_index("idx_product_variants_product", "product_variants", ["product_id"])
    op.create_index("idx_product_variants_type", "product_variants", ["variant_type"])
    op.create_index("idx_product_variants_availability", "product_variants", ["product_id", "is_available"])


def downgrade() -> None:
    op.drop_index("idx_product_variants_availability", table_name="product_variants")
    op.drop_index("idx_product_variants_type", table_name="product_variants")
    op.drop_index("idx_product_variants_product", table_name="product_variants")
    op.drop_table("product_variants")
    op.execute("DROP TRIGGER IF EXISTS trg_update_product_search_text ON products")
    op.execute("DROP FUNCTION IF EXISTS update_product_search_text")
    op.drop_index("idx_products_search", table_name="products")
    op.drop_index("idx_products_org_status", table_name="products")
    op.drop_index("idx_products_status_visibility", table_name="products")
    op.drop_index("idx_products_category", table_name="products")
    op.drop_table("products")
    op.drop_index("idx_product_categories_active", table_name="product_categories")
    op.drop_index("idx_product_categories_parent", table_name="product_categories")
    op.drop_table("product_categories")

