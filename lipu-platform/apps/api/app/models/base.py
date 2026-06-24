"""Declarative SQLAlchemy base classes."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, MetaData, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base metadata shared by all ORM models."""

    metadata = MetaData(naming_convention=convention)


class UUIDPrimaryKeyMixin:
    """UUID primary key for PostgreSQL-backed entities."""

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )


class TimestampMixin:
    """Created and updated timestamps stored in UTC by the database."""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class BaseModel(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Abstract base for most persistent domain entities."""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__
        chars: list[str] = []
        for index, char in enumerate(name):
            if char.isupper() and index:
                chars.append("_")
            chars.append(char.lower())
        return "".join(chars)

    def as_dict(self) -> dict[str, Any]:
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
