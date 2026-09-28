"""Channels Ecotech may later use to talk with a person."""

from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID as PythonUUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import (
    CommunicationEventType,
    ConversationChannel,
    ConversationStatus,
    MessageSender,
    sql_in,
)
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.lead import Lead
    from app.models.user import User


class Conversation(BaseModel):
    """A thread that can belong to a user, a lead, or both."""

    __tablename__ = "conversations"
    __table_args__ = (
        CheckConstraint(
            sql_in("origin_channel", ConversationChannel), name="ck_conversations_origin_channel"
        ),
        CheckConstraint(sql_in("status", ConversationStatus), name="ck_conversations_status"),
        CheckConstraint(
            "user_id IS NOT NULL OR lead_id IS NOT NULL", name="ck_conversations_has_participant"
        ),
        Index("idx_conversations_user", "user_id"),
        Index("idx_conversations_lead", "lead_id"),
    )

    user_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    lead_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
    )
    origin_channel: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(
        String(16), default=ConversationStatus.OPEN.value, nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="conversations", foreign_keys=[user_id])
    lead: Mapped["Lead"] = relationship(back_populates="conversations")
    messages: Mapped[list["ConversationMessage"]] = relationship(back_populates="conversation")


class ConversationMessage(BaseModel):
    """One message on a conversation, tagged with the channel it used."""

    __tablename__ = "conversation_messages"
    __table_args__ = (
        CheckConstraint(sql_in("sender", MessageSender), name="ck_conversation_messages_sender"),
        CheckConstraint(
            sql_in("channel", ConversationChannel), name="ck_conversation_messages_channel"
        ),
        Index("idx_conversation_messages_conversation", "conversation_id", "created_at"),
    )

    conversation_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )
    sender: Mapped[str] = mapped_column(String(16), nullable=False)
    channel: Mapped[str] = mapped_column(String(16), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    message_metadata: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        default=dict,
        server_default=text("'{}'::jsonb"),
        nullable=False,
    )
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")


class CommunicationEvent(BaseModel):
    """A lightweight record that something was received, sent, or changed."""

    __tablename__ = "communication_events"
    __table_args__ = (
        CheckConstraint(
            sql_in("event_type", CommunicationEventType), name="ck_communication_events_event_type"
        ),
        CheckConstraint(
            f"channel IS NULL OR {sql_in('channel', ConversationChannel)}",
            name="ck_communication_events_channel",
        ),
        Index("idx_communication_events_lead", "lead_id", "created_at"),
        Index("idx_communication_events_type", "event_type"),
    )

    user_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    lead_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
    )
    conversation_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True,
    )
    event_type: Mapped[str] = mapped_column(String(40), nullable=False)
    channel: Mapped[str | None] = mapped_column(String(16), nullable=True)
    event_metadata: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        default=dict,
        server_default=text("'{}'::jsonb"),
        nullable=False,
    )

    lead: Mapped["Lead"] = relationship(back_populates="communication_events")
    user: Mapped["User"] = relationship(foreign_keys=[user_id])
    conversation: Mapped["Conversation"] = relationship()
