"""Foundation tests for schema validation and the database client."""

from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.api.v1.boundaries import API_BOUNDARIES
from app.db.session import AsyncSessionLocal, engine
from app.domain.enums import (
    LeadSource,
    LeadStatus,
    ProductArea,
    ProjectType,
    TransformStatus,
    TransformTarget,
)
from app.models import Base
from app.schemas.platform import (
    ConsultationRequestCreate,
    LeadCreate,
    ProductInterestCreate,
    ProjectCreate,
    TransformRequestCreate,
)
from app.schemas.user import UserCreate
from app.services.platform import consultation_from_website_form, lead_from_consultation


def test_database_client_is_configured_without_connecting() -> None:
    assert engine is not None
    assert AsyncSessionLocal is not None
    assert engine.dialect.name == "postgresql"
    assert "password" not in engine.url.render_as_string(hide_password=True)


def test_platform_tables_are_registered() -> None:
    names = set(Base.metadata.tables)
    expected = {
        "user_profiles",
        "leads",
        "consultation_requests",
        "projects",
        "product_interests",
        "transform_requests",
        "transform_assets",
        "transform_results",
        "conversations",
        "conversation_messages",
        "communication_events",
    }
    assert expected <= names
    assert "password" not in Base.metadata.tables["users"].columns
    assert "password_hash" in Base.metadata.tables["users"].columns
    assert "bytea" not in {
        column.type.__class__.__name__.lower()
        for column in Base.metadata.tables["transform_assets"].columns
    }


def test_user_schema_does_not_accept_a_password() -> None:
    assert "password" not in UserCreate.model_fields
    assert "password_hash" not in UserCreate.model_fields


def test_consultation_accepts_the_current_website_form_without_an_account() -> None:
    consultation = consultation_from_website_form(
        {
            "firstName": "Asha",
            "lastName": "Rao",
            "email": "asha@example.com",
            "phone": "+91 98765 43210",
            "city": "Bhubaneswar",
            "projectType": "residential",
            "message": "We want larger openings in the living room.",
        }
    )
    assert consultation.user_id is None
    assert consultation.project_type is ProjectType.RESIDENTIAL
    assert consultation.location == "Bhubaneswar"


def test_consultation_rejects_invalid_email_and_unknown_project_type() -> None:
    with pytest.raises(ValidationError):
        ConsultationRequestCreate.model_validate(
            {
                "first_name": "Asha",
                "last_name": "Rao",
                "email": "not-an-email",
                "project_type": ProjectType.RESIDENTIAL,
                "location": "Bhubaneswar",
                "message": "Hello",
            }
        )
    with pytest.raises(ValidationError):
        consultation_from_website_form(
            {
                "firstName": "Asha",
                "lastName": "Rao",
                "email": "asha@example.com",
                "city": "Bhubaneswar",
                "projectType": "unknown",
                "message": "Hello",
            }
        )


def test_lead_validation_and_guest_link_from_consultation() -> None:
    consultation = consultation_from_website_form(
        {
            "firstName": "Asha",
            "lastName": "Rao",
            "email": "asha@example.com",
            "city": "Puri",
            "projectType": "commercial",
            "message": "A cafe front.",
        }
    )
    lead = lead_from_consultation(consultation)
    assert lead.user_id is None
    assert lead.source is LeadSource.CONSULTATION
    assert lead.status is LeadStatus.NEW
    assert lead.name == "Asha Rao"
    with pytest.raises(ValidationError):
        LeadCreate(source=LeadSource.WEBSITE, name=" ", email="asha@example.com")


def test_project_and_transform_enums() -> None:
    project = ProjectCreate(
        name="Lake house", project_type=ProjectType.HOSPITALITY, location="Cuttack"
    )
    assert project.status.value == "DRAFT"
    with pytest.raises(ValidationError):
        ProjectCreate(name="Lake house", project_type="FACTORY")  # type: ignore[arg-type]

    request = TransformRequestCreate(
        target=TransformTarget.BALCONY, status=TransformStatus.CONFIGURED
    )
    assert request.user_id is None
    with pytest.raises(ValidationError):
        TransformRequestCreate(target="ROOF")  # type: ignore[arg-type]


def test_product_interest_requires_an_owner() -> None:
    with pytest.raises(ValidationError):
        ProductInterestCreate(area=ProductArea.WINDOWS)
    interest = ProductInterestCreate(area=ProductArea.DOORS, lead_id=uuid4())
    assert interest.user_id is None


def test_api_boundaries_stay_client_independent() -> None:
    assert API_BOUNDARIES["consultations"] == ("/api/v1/consultations",)
    assert API_BOUNDARIES["transform"] == ("/api/v1/transform/requests",)
    assert all(path.startswith("/api/v1/") for paths in API_BOUNDARIES.values() for path in paths)
