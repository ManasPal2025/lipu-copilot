"""create ecotech platform foundation

Revision ID: 0004_create_ecotech_platform
Revises: 0003_create_quotes
Create Date: 2026-09-23
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.domain.enums import (
    CommunicationEventType,
    ContactMethod,
    ConversationChannel,
    ConversationStatus,
    LeadPriority,
    LeadSource,
    LeadStatus,
    MessageSender,
    ProductArea,
    ProjectStatus,
    ProjectType,
    TransformAssetType,
    TransformStatus,
    TransformTarget,
    TransformVariant,
    sql_in,
)


revision: str = "0004_create_ecotech_platform"
down_revision: str | None = "0003_create_quotes"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _uuid(name: str, *, nullable: bool) -> sa.Column:
    return sa.Column(name, postgresql.UUID(as_uuid=True), nullable=nullable)


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    ]


def _id() -> sa.Column:
    return sa.Column(
        "id",
        postgresql.UUID(as_uuid=True),
        primary_key=True,
        server_default=sa.text("gen_random_uuid()"),
    )


def upgrade() -> None:
    op.add_column("users", sa.Column("password_hash", sa.String(length=255), nullable=True))

    op.create_table(
        "user_profiles",
        _id(),
        _uuid("user_id", nullable=False),
        sa.Column("display_name", sa.String(length=160), nullable=True),
        sa.Column("preferred_contact_method", sa.String(length=16), nullable=True),
        sa.Column("city", sa.String(length=120), nullable=True),
        sa.Column("state", sa.String(length=120), nullable=True),
        sa.Column("company", sa.String(length=160), nullable=True),
        sa.Column("project_interests", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'[]'::jsonb")),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_user_profiles"),
        sa.UniqueConstraint("user_id", name="uq_user_profiles_user_id"),
        sa.CheckConstraint(
            f"preferred_contact_method IS NULL OR {sql_in('preferred_contact_method', ContactMethod)}",
            name="ck_user_profiles_preferred_contact_method",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_user_profiles_user_id_users", ondelete="CASCADE"),
    )

    op.create_table(
        "leads",
        _id(),
        _uuid("user_id", nullable=True),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="NEW"),
        sa.Column("priority", sa.String(length=16), nullable=False, server_default="NORMAL"),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("location", sa.String(length=160), nullable=True),
        sa.Column("project_summary", sa.Text(), nullable=True),
        _uuid("created_by_id", nullable=True),
        _uuid("updated_by_id", nullable=True),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_leads"),
        sa.CheckConstraint(sql_in("source", LeadSource), name="ck_leads_source"),
        sa.CheckConstraint(sql_in("status", LeadStatus), name="ck_leads_status"),
        sa.CheckConstraint(sql_in("priority", LeadPriority), name="ck_leads_priority"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_leads_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], name="fk_leads_created_by_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["updated_by_id"], ["users.id"], name="fk_leads_updated_by_id_users", ondelete="SET NULL"),
    )
    op.create_index("idx_leads_status", "leads", ["status"])
    op.create_index("idx_leads_source", "leads", ["source"])
    op.create_index("idx_leads_email", "leads", ["email"])
    op.create_index("idx_leads_user", "leads", ["user_id"])

    op.create_table(
        "consultation_requests",
        _id(),
        _uuid("user_id", nullable=True),
        _uuid("lead_id", nullable=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("project_type", sa.String(length=32), nullable=False),
        sa.Column("location", sa.String(length=160), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("approximate_size", sa.String(length=120), nullable=True),
        sa.Column("preferred_contact_method", sa.String(length=16), nullable=True),
        sa.Column("preferred_callback_time", sa.String(length=120), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="NEW"),
        _uuid("created_by_id", nullable=True),
        _uuid("updated_by_id", nullable=True),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_consultation_requests"),
        sa.CheckConstraint(sql_in("project_type", ProjectType), name="ck_consultation_requests_project_type"),
        sa.CheckConstraint(sql_in("status", LeadStatus), name="ck_consultation_requests_status"),
        sa.CheckConstraint(
            f"preferred_contact_method IS NULL OR {sql_in('preferred_contact_method', ContactMethod)}",
            name="ck_consultation_requests_preferred_contact_method",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_consultation_requests_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], name="fk_consultation_requests_lead_id_leads", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], name="fk_consultations_created_by_id", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["updated_by_id"], ["users.id"], name="fk_consultations_updated_by_id", ondelete="SET NULL"),
    )
    op.create_index("idx_consultation_requests_email", "consultation_requests", ["email"])
    op.create_index("idx_consultation_requests_status", "consultation_requests", ["status"])
    op.create_index("idx_consultation_requests_user", "consultation_requests", ["user_id"])
    op.create_index("idx_consultation_requests_lead", "consultation_requests", ["lead_id"])

    op.create_table(
        "projects",
        _id(),
        _uuid("user_id", nullable=True),
        _uuid("lead_id", nullable=True),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("project_type", sa.String(length=32), nullable=False),
        sa.Column("location", sa.String(length=160), nullable=True),
        sa.Column("budget_range", sa.String(length=80), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="DRAFT"),
        sa.Column("requirements", sa.Text(), nullable=True),
        _uuid("created_by_id", nullable=True),
        _uuid("updated_by_id", nullable=True),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_projects"),
        sa.CheckConstraint(sql_in("project_type", ProjectType), name="ck_projects_project_type"),
        sa.CheckConstraint(sql_in("status", ProjectStatus), name="ck_projects_status"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_projects_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], name="fk_projects_lead_id_leads", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], name="fk_projects_created_by_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["updated_by_id"], ["users.id"], name="fk_projects_updated_by_id_users", ondelete="SET NULL"),
    )
    op.create_index("idx_projects_status", "projects", ["status"])
    op.create_index("idx_projects_user", "projects", ["user_id"])
    op.create_index("idx_projects_lead", "projects", ["lead_id"])

    op.create_table(
        "product_interests",
        _id(),
        _uuid("user_id", nullable=True),
        _uuid("lead_id", nullable=True),
        _uuid("consultation_request_id", nullable=True),
        _uuid("project_id", nullable=True),
        _uuid("product_id", nullable=True),
        sa.Column("area", sa.String(length=32), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_product_interests"),
        sa.CheckConstraint(sql_in("area", ProductArea), name="ck_product_interests_area"),
        sa.CheckConstraint(
            "user_id IS NOT NULL OR lead_id IS NOT NULL OR consultation_request_id IS NOT NULL OR project_id IS NOT NULL",
            name="ck_product_interests_has_owner",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_product_interests_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], name="fk_product_interests_lead_id_leads", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(
            ["consultation_request_id"],
            ["consultation_requests.id"],
            name="fk_product_interests_consultation_id",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], name="fk_product_interests_project_id_projects", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], name="fk_product_interests_product_id_products", ondelete="SET NULL"),
    )
    op.create_index("idx_product_interests_user", "product_interests", ["user_id"])
    op.create_index("idx_product_interests_lead", "product_interests", ["lead_id"])
    op.create_index("idx_product_interests_consultation", "product_interests", ["consultation_request_id"])

    op.create_table(
        "transform_requests",
        _id(),
        _uuid("user_id", nullable=True),
        _uuid("lead_id", nullable=True),
        sa.Column("target", sa.String(length=16), nullable=False),
        sa.Column("variant", sa.String(length=32), nullable=True),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="UPLOADED"),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_transform_requests"),
        sa.CheckConstraint(sql_in("target", TransformTarget), name="ck_transform_requests_target"),
        sa.CheckConstraint(sql_in("status", TransformStatus), name="ck_transform_requests_status"),
        sa.CheckConstraint(
            f"variant IS NULL OR {sql_in('variant', TransformVariant)}",
            name="ck_transform_requests_variant",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_transform_requests_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], name="fk_transform_requests_lead_id_leads", ondelete="SET NULL"),
    )
    op.create_index("idx_transform_requests_user", "transform_requests", ["user_id"])
    op.create_index("idx_transform_requests_status", "transform_requests", ["status"])

    op.create_table(
        "transform_assets",
        _id(),
        _uuid("transform_request_id", nullable=False),
        sa.Column("asset_type", sa.String(length=16), nullable=False),
        sa.Column("storage_key", sa.String(length=500), nullable=False),
        sa.Column("mime_type", sa.String(length=120), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_transform_assets"),
        sa.CheckConstraint(sql_in("asset_type", TransformAssetType), name="ck_transform_assets_asset_type"),
        sa.ForeignKeyConstraint(
            ["transform_request_id"],
            ["transform_requests.id"],
            name="fk_transform_assets_request_id",
            ondelete="CASCADE",
        ),
    )
    op.create_index("idx_transform_assets_request", "transform_assets", ["transform_request_id"])

    op.create_table(
        "transform_results",
        _id(),
        _uuid("transform_request_id", nullable=False),
        _uuid("result_asset_id", nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_transform_results"),
        sa.UniqueConstraint("transform_request_id", name="uq_transform_results_transform_request_id"),
        sa.ForeignKeyConstraint(
            ["transform_request_id"],
            ["transform_requests.id"],
            name="fk_transform_results_request_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["result_asset_id"],
            ["transform_assets.id"],
            name="fk_transform_results_asset_id",
            ondelete="SET NULL",
        ),
    )

    op.create_table(
        "conversations",
        _id(),
        _uuid("user_id", nullable=True),
        _uuid("lead_id", nullable=True),
        sa.Column("origin_channel", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False, server_default="OPEN"),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_conversations"),
        sa.CheckConstraint(sql_in("origin_channel", ConversationChannel), name="ck_conversations_origin_channel"),
        sa.CheckConstraint(sql_in("status", ConversationStatus), name="ck_conversations_status"),
        sa.CheckConstraint("user_id IS NOT NULL OR lead_id IS NOT NULL", name="ck_conversations_has_participant"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_conversations_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], name="fk_conversations_lead_id_leads", ondelete="SET NULL"),
    )
    op.create_index("idx_conversations_user", "conversations", ["user_id"])
    op.create_index("idx_conversations_lead", "conversations", ["lead_id"])

    op.create_table(
        "conversation_messages",
        _id(),
        _uuid("conversation_id", nullable=False),
        sa.Column("sender", sa.String(length=16), nullable=False),
        sa.Column("channel", sa.String(length=16), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_conversation_messages"),
        sa.CheckConstraint(sql_in("sender", MessageSender), name="ck_conversation_messages_sender"),
        sa.CheckConstraint(sql_in("channel", ConversationChannel), name="ck_conversation_messages_channel"),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
            name="fk_conversation_messages_conversation_id",
            ondelete="CASCADE",
        ),
    )
    op.create_index("idx_conversation_messages_conversation", "conversation_messages", ["conversation_id", "created_at"])

    op.create_table(
        "communication_events",
        _id(),
        _uuid("user_id", nullable=True),
        _uuid("lead_id", nullable=True),
        _uuid("conversation_id", nullable=True),
        sa.Column("event_type", sa.String(length=40), nullable=False),
        sa.Column("channel", sa.String(length=16), nullable=True),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        *_timestamps(),
        sa.PrimaryKeyConstraint("id", name="pk_communication_events"),
        sa.CheckConstraint(sql_in("event_type", CommunicationEventType), name="ck_communication_events_event_type"),
        sa.CheckConstraint(
            f"channel IS NULL OR {sql_in('channel', ConversationChannel)}",
            name="ck_communication_events_channel",
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_communication_events_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], name="fk_communication_events_lead_id_leads", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"],
            name="fk_communication_events_conversation_id",
            ondelete="SET NULL",
        ),
    )
    op.create_index("idx_communication_events_lead", "communication_events", ["lead_id", "created_at"])
    op.create_index("idx_communication_events_type", "communication_events", ["event_type"])


def downgrade() -> None:
    op.drop_table("communication_events")
    op.drop_table("conversation_messages")
    op.drop_table("conversations")
    op.drop_table("transform_results")
    op.drop_table("transform_assets")
    op.drop_table("transform_requests")
    op.drop_table("product_interests")
    op.drop_table("projects")
    op.drop_table("consultation_requests")
    op.drop_table("leads")
    op.drop_table("user_profiles")
    op.drop_column("users", "password_hash")
