"""Organization request and response schemas."""

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import EmailStr, Field, field_validator

from app.schemas.base import APIModel


OrganizationStatus = Literal["active", "inactive", "suspended"]


class OrganizationBase(APIModel):
    name: str = Field(min_length=2, max_length=255)
    slug: str = Field(min_length=2, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: str | None = None
    logo_url: str | None = Field(default=None, max_length=500)
    website_url: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    address: dict[str, Any] | None = None
    founded_year: int | None = Field(default=None, ge=1800, le=2100)
    industry: str | None = Field(default=None, max_length=100)
    status: OrganizationStatus = "active"
    settings: dict[str, Any] = Field(default_factory=dict)

    @field_validator("name", "slug")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty.")
        return value


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(APIModel):
    name: str | None = Field(default=None, min_length=2, max_length=255)
    slug: str | None = Field(default=None, min_length=2, max_length=255, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    description: str | None = None
    logo_url: str | None = Field(default=None, max_length=500)
    website_url: str | None = Field(default=None, max_length=500)
    phone: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    address: dict[str, Any] | None = None
    founded_year: int | None = Field(default=None, ge=1800, le=2100)
    industry: str | None = Field(default=None, max_length=100)
    status: OrganizationStatus | None = None
    settings: dict[str, Any] | None = None

    @field_validator("name", "slug")
    @classmethod
    def strip_optional_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be empty.")
        return value


class OrganizationRead(OrganizationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
