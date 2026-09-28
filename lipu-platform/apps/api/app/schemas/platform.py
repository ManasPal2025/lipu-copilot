"""Request validation for the Ecotech platform domains."""

import re
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import ConfigDict, EmailStr, Field, field_validator, model_validator

from app.domain.enums import (
    ContactMethod,
    ConversationChannel,
    LeadPriority,
    LeadSource,
    LeadStatus,
    MessageSender,
    ProductArea,
    ProjectStatus,
    ProjectType,
    TransformStatus,
    TransformTarget,
    TransformVariant,
)
from app.schemas.base import APIModel

_PHONE = re.compile(r"^\+?[0-9][0-9\s\-()]{6,18}$")


def _clean_name(value: str) -> str:
    cleaned = " ".join(value.split())
    if not cleaned:
        raise ValueError("Name is required.")
    return cleaned


def _clean_phone(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    if not _PHONE.fullmatch(cleaned):
        raise ValueError("Enter a valid phone number.")
    digits = re.sub(r"\D", "", cleaned)
    if not 8 <= len(digits) <= 15:
        raise ValueError("Enter a valid phone number.")
    return cleaned


class LeadCreate(APIModel):
    user_id: UUID | None = None
    source: LeadSource
    status: LeadStatus = LeadStatus.NEW
    priority: LeadPriority = LeadPriority.NORMAL
    name: str = Field(min_length=1, max_length=160)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=32)
    location: str | None = Field(default=None, max_length=160)
    project_summary: str | None = Field(default=None, max_length=4000)

    @field_validator("name", "location", "project_summary")
    @classmethod
    def clean_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _clean_name(value)

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, value: str | None) -> str | None:
        return _clean_phone(value)


_WEBSITE_PROJECT_TYPES = {
    "residential": ProjectType.RESIDENTIAL,
    "renovation": ProjectType.RENOVATION,
    "commercial": ProjectType.COMMERCIAL,
    "architect": ProjectType.ARCHITECT,
}


class ConsultationSubmission(APIModel):
    """Public consultation contract.

    Guests omit user_id. A user_id in the body is never trusted: the route
    derives ownership from the Clerk session. Historical guest enquiries are
    not attached when someone later creates an account with the same email.
    """

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=32)
    city: str = Field(min_length=1, max_length=160)
    project_type: ProjectType
    message: str = Field(min_length=1, max_length=4000)
    user_id: UUID | None = None

    @field_validator("project_type", mode="before")
    @classmethod
    def accept_website_project_type(cls, value: object) -> object:
        if isinstance(value, str):
            mapped = _WEBSITE_PROJECT_TYPES.get(value.strip().lower())
            return mapped if mapped is not None else value.strip().upper()
        return value

    @field_validator("first_name", "last_name", "city")
    @classmethod
    def clean_required_text(cls, value: str) -> str:
        return _clean_name(value)

    @field_validator("message")
    @classmethod
    def clean_message(cls, value: str) -> str:
        cleaned = " ".join(value.split())
        if not cleaned:
            raise ValueError("Message is required.")
        return cleaned

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, value: str | None) -> str | None:
        return _clean_phone(value)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class ConsultationAccepted(APIModel):
    success: bool = True
    consultation_id: UUID
    lead_id: UUID
    status: LeadStatus
    message: str


class ConsultationHistoryItem(APIModel):
    """A customer's own enquiry. Internal lead and staff fields stay off this contract."""

    id: UUID
    created_at: datetime
    project_type: str
    city: str
    status: str
    message: str


class ConsultationHistoryPage(APIModel):
    items: list[ConsultationHistoryItem]
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=50)
    total: int = Field(ge=0)
    has_next: bool


class ConsultationRequestCreate(APIModel):
    """Fields match the current consultation form, with optional account linkage."""

    user_id: UUID | None = None
    lead_id: UUID | None = None
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=32)
    project_type: ProjectType
    location: str = Field(min_length=1, max_length=160)
    message: str = Field(min_length=1, max_length=4000)
    approximate_size: str | None = Field(default=None, max_length=120)
    preferred_contact_method: ContactMethod | None = None
    preferred_callback_time: str | None = Field(default=None, max_length=120)
    status: LeadStatus = LeadStatus.NEW

    @field_validator("first_name", "last_name", "location")
    @classmethod
    def clean_required_text(cls, value: str) -> str:
        return _clean_name(value)

    @field_validator("message", "approximate_size", "preferred_callback_time")
    @classmethod
    def clean_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = " ".join(value.split())
        return cleaned or None

    @field_validator("phone")
    @classmethod
    def clean_phone(cls, value: str | None) -> str | None:
        return _clean_phone(value)


class ProjectCreate(APIModel):
    user_id: UUID | None = None
    lead_id: UUID | None = None
    name: str = Field(min_length=1, max_length=160)
    project_type: ProjectType
    location: str | None = Field(default=None, max_length=160)
    budget_range: str | None = Field(default=None, max_length=80)
    status: ProjectStatus = ProjectStatus.DRAFT
    requirements: str | None = Field(default=None, max_length=4000)

    @field_validator("name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        return _clean_name(value)

    @field_validator("location", "budget_range", "requirements")
    @classmethod
    def clean_optional(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = " ".join(value.split())
        return cleaned or None


class ProductInterestCreate(APIModel):
    user_id: UUID | None = None
    lead_id: UUID | None = None
    consultation_request_id: UUID | None = None
    project_id: UUID | None = None
    product_id: UUID | None = None
    area: ProductArea
    note: str | None = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def require_owner(self) -> "ProductInterestCreate":
        if not any((self.user_id, self.lead_id, self.consultation_request_id, self.project_id)):
            raise ValueError(
                "A product interest must belong to a user, lead, consultation, or project."
            )
        return self


class TransformHistoryAsset(APIModel):
    """A customer-visible file pointer. Internal storage keys stay on the server."""

    id: UUID
    mime_type: str
    public_url: str | None = None


class TransformHistoryResult(APIModel):
    id: UUID
    created_at: datetime
    asset: TransformHistoryAsset | None = None


class TransformHistoryItem(APIModel):
    id: UUID
    created_at: datetime
    target: str
    variant: str | None = None
    status: str
    source_asset: TransformHistoryAsset | None = None
    result: TransformHistoryResult | None = None


class TransformHistoryPage(APIModel):
    items: list[TransformHistoryItem]
    page: int = Field(ge=1)
    page_size: int = Field(ge=1, le=50)
    total: int = Field(ge=0)
    has_next: bool


class TransformSourceSubmission(APIModel):
    """Customer source pointer. Ownership, status, and storage keys stay on the server."""

    model_config = ConfigDict(extra="forbid", from_attributes=True, populate_by_name=True)

    mime_type: Literal["image/jpeg", "image/png", "image/webp"]
    source_kind: Literal["UPLOAD", "SAMPLE"]
    sample_id: Literal["living", "balcony", "apartment", "villa"] | None = None

    @model_validator(mode="after")
    def match_sample(self) -> "TransformSourceSubmission":
        if self.source_kind == "SAMPLE" and self.sample_id is None:
            raise ValueError("A sample image is required.")
        if self.source_kind == "UPLOAD" and self.sample_id is not None:
            raise ValueError("An upload cannot name a sample image.")
        return self


class TransformRequestSubmission(APIModel):
    """Fields a signed-in customer may send. The session supplies the user."""

    model_config = ConfigDict(extra="forbid", from_attributes=True, populate_by_name=True)

    target: TransformTarget
    variant: TransformVariant | None = None
    source_asset: TransformSourceSubmission


class TransformRequestAccepted(APIModel):
    id: UUID
    created_at: datetime
    target: str
    variant: str | None = None
    status: str


class TransformConfigure(APIModel):
    """Target and variant only. Status, prompts, and storage keys stay on the server."""

    model_config = ConfigDict(extra="forbid", from_attributes=True, populate_by_name=True)

    target: TransformTarget
    variant: TransformVariant | None = None


class TransformPipelineAsset(APIModel):
    id: UUID
    mime_type: str
    public_url: str | None = None


class TransformPipelineView(APIModel):
    id: UUID
    status: str
    target: str
    variant: str | None = None
    result: TransformPipelineAsset | None = None


class TransformRequestCreate(APIModel):
    user_id: UUID | None = None
    lead_id: UUID | None = None
    target: TransformTarget
    variant: TransformVariant | None = None
    status: TransformStatus = TransformStatus.UPLOADED


class TransformAssetCreate(APIModel):
    transform_request_id: UUID
    asset_type: str = Field(pattern="^(SOURCE|RESULT|REFERENCE)$")
    storage_key: str = Field(min_length=1, max_length=500)
    mime_type: str = Field(min_length=1, max_length=120)


class ConversationMessageCreate(APIModel):
    conversation_id: UUID
    sender: MessageSender
    channel: ConversationChannel
    body: str = Field(min_length=1, max_length=8000)
