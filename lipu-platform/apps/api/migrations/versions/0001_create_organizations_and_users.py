"""create organizations and users

Revision ID: 0001_create_organizations_and_users
Revises: None
Create Date: 2026-06-24
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0001_create_organizations_and_users"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("logo_url", sa.String(length=500), nullable=True),
        sa.Column("website_url", sa.String(length=500), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("address", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("founded_year", sa.Integer(), nullable=True),
        sa.Column("industry", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("settings", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name="pk_organizations"),
        sa.UniqueConstraint("name", name="uq_organizations_name"),
        sa.UniqueConstraint("slug", name="uq_organizations_slug"),
    )
    op.create_index("idx_organizations_slug", "organizations", ["slug"])
    op.create_index("idx_organizations_status", "organizations", ["status"])

    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("clerk_id", sa.String(length=255), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=True),
        sa.Column("last_name", sa.String(length=100), nullable=True),
        sa.Column("avatar_url", sa.String(length=500), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("permissions", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        sa.Column("profile", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("login_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name="fk_users_organization_id_organizations",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("clerk_id", name="uq_users_clerk_id"),
        sa.UniqueConstraint("clerk_id", "email", name="uq_users_clerk_email"),
    )
    op.create_index("idx_users_organization_role", "users", ["organization_id", "role"])
    op.create_index("idx_users_status", "users", ["status"])


def downgrade() -> None:
    op.drop_index("idx_users_status", table_name="users")
    op.drop_index("idx_users_organization_role", table_name="users")
    op.drop_table("users")
    op.drop_index("idx_organizations_status", table_name="organizations")
    op.drop_index("idx_organizations_slug", table_name="organizations")
    op.drop_table("organizations")

