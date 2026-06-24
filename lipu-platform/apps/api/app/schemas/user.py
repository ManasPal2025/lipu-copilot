"""User request and response schemas."""

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import EmailStr, Field, field_validator

from app.schemas.base import APIModel


UserRole = Literal["admin", "sales", "customer", "guest"]
UserStatus = Literal["active", "inactive", "suspended"]


class UserBase(APIModel):
    clerk_id: str = Field(min_length=3, max_length=255)
    organization_id: UUID
    email: EmailStr
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    avatar_url: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)
    role: UserRole
    permissions: list[str] = Field(default_factory=list)
    profile: dict[str, Any] = Field(default_factory=dict)
    status: UserStatus = "active"

    @field_validator("clerk_id")
    @classmethod
    def strip_clerk_id(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Clerk ID cannot be empty.")
        return value

    @field_validator("permissions")
    @classmethod
    def normalize_permissions(cls, value: list[str]) -> list[str]:
        return sorted({permission.strip() for permission in value if permission.strip()})


class UserCreate(UserBase):
    pass


class UserUpdate(APIModel):
    organization_id: UUID | None = None
    email: EmailStr | None = None
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    avatar_url: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)
    role: UserRole | None = None
    permissions: list[str] | None = None
    profile: dict[str, Any] | None = None
    status: UserStatus | None = None

    @field_validator("permissions")
    @classmethod
    def normalize_permissions(cls, value: list[str] | None) -> list[str] | None:
        if value is None:
            return None
        return sorted({permission.strip() for permission in value if permission.strip()})

    @field_validator("first_name", "last_name", "phone")
    @classmethod
    def strip_optional_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip() or None


class UserRead(UserBase):
    id: UUID
    last_login: datetime | None = None
    login_count: int
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
