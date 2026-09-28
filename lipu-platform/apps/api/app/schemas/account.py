"""Authenticated account contracts.

Clients may update profile details. Role, Clerk id, organization, and any
password field are not part of this contract.
"""

from datetime import datetime
from uuid import UUID

from pydantic import Field, field_validator

from app.domain.enums import ContactMethod, ProjectType
from app.schemas.base import APIModel
from app.schemas.platform import _clean_phone


def _optional_text(value: str | None, limit: int) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(value.split())
    if not cleaned:
        return None
    if len(cleaned) > limit:
        raise ValueError(f"Use {limit} characters or fewer.")
    return cleaned


class ProfileRead(APIModel):
    display_name: str | None = None
    preferred_contact_method: str | None = None
    city: str | None = None
    state: str | None = None
    company: str | None = None
    project_interests: list[str] = Field(default_factory=list)


class MeRead(APIModel):
    id: UUID
    clerk_id: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    avatar_url: str | None = None
    role: str
    created_at: datetime
    profile: ProfileRead


class ProfileUpdate(APIModel):
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    city: str | None = Field(default=None, max_length=120)
    state: str | None = Field(default=None, max_length=120)
    company: str | None = Field(default=None, max_length=160)
    preferred_contact_method: ContactMethod | None = None
    project_interests: list[ProjectType] | None = None

    @field_validator("first_name", "last_name")
    @classmethod
    def clean_name(cls, value: str | None) -> str | None:
        return _optional_text(value, 100)

    @field_validator("city", "state")
    @classmethod
    def clean_place(cls, value: str | None) -> str | None:
        return _optional_text(value, 120)

    @field_validator("company")
    @classmethod
    def clean_company(cls, value: str | None) -> str | None:
        return _optional_text(value, 160)

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, value: str | None) -> str | None:
        cleaned = _clean_phone(value)
        if cleaned and len(cleaned) > 20:
            raise ValueError("Enter a valid phone number.")
        return cleaned

    @field_validator("project_interests")
    @classmethod
    def unique_interests(cls, value: list[ProjectType] | None) -> list[ProjectType] | None:
        if value is None:
            return None
        unique: list[ProjectType] = []
        for item in value:
            if item not in unique:
                unique.append(item)
        if len(unique) > 8:
            raise ValueError("Choose up to 8 interests.")
        return unique
