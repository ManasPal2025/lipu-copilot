"""Application services for platform records.

These functions validate input and describe how a future repository will persist it.
They do not send WhatsApp or generate images.
"""

from app.domain.enums import LeadSource, LeadStatus
from app.schemas.platform import ConsultationRequestCreate, ConsultationSubmission, LeadCreate


def consultation_from_website_form(payload: dict[str, object]) -> ConsultationRequestCreate:
    """Map the current contact form onto a guest consultation request."""

    submission = ConsultationSubmission.model_validate(
        {
            "user_id": payload.get("userId"),
            "first_name": payload.get("firstName"),
            "last_name": payload.get("lastName"),
            "email": payload.get("email"),
            "phone": payload.get("phone") or None,
            "city": payload.get("city"),
            "project_type": payload.get("projectType"),
            "message": payload.get("message"),
        }
    )
    return ConsultationRequestCreate(
        user_id=submission.user_id,
        first_name=submission.first_name,
        last_name=submission.last_name,
        email=submission.email,
        phone=submission.phone,
        project_type=submission.project_type,
        location=submission.city,
        message=submission.message,
    )


def lead_from_consultation(
    consultation: ConsultationRequestCreate, source: LeadSource = LeadSource.CONSULTATION
) -> LeadCreate:
    """Build the lead a consultation will belong to. Guests have no user id."""

    return LeadCreate(
        user_id=consultation.user_id,
        source=source,
        status=LeadStatus.NEW,
        name=f"{consultation.first_name} {consultation.last_name}",
        email=consultation.email,
        phone=consultation.phone,
        location=consultation.location,
        project_summary=consultation.message,
    )
