"""Persist a consultation and its lead in one transaction, then send email."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppError
from app.core.logging import get_logger
from app.domain.enums import (
    CommunicationEventType,
    ConversationChannel,
    LeadPriority,
    LeadSource,
    LeadStatus,
)
from app.models.communication import CommunicationEvent
from app.models.consultation_request import ConsultationRequest
from app.models.lead import Lead
from app.schemas.platform import (
    ConsultationAccepted,
    ConsultationHistoryItem,
    ConsultationHistoryPage,
    ConsultationSubmission,
)
from app.services.base import BaseService
from app.services.email import (
    ConsultationEmailContext,
    EmailAttempt,
    EmailService,
    build_email_service,
    utc_now,
)


logger = get_logger(__name__)

_CLOSED = {LeadStatus.WON.value, LeadStatus.LOST.value, LeadStatus.CLOSED.value}
_CONFIRMATION = "Your consultation request has been received."


class ConsultationService(BaseService):
    def __init__(self, session: AsyncSession, email_service: EmailService | None = None) -> None:
        super().__init__(session)
        self.email_service = email_service if email_service is not None else build_email_service()

    async def submit(
        self,
        payload: ConsultationSubmission,
        authenticated_user_id: UUID | None = None,
    ) -> ConsultationAccepted:
        # Ownership comes from the verified session. payload.user_id is ignored
        # so a browser cannot attach the enquiry to someone else. Guest rows
        # already stored with a null user_id are not backfilled here.
        owner_id = authenticated_user_id
        try:
            email = str(payload.email)
            lead = await self._open_lead(email)
            created_lead = lead is None
            if lead is None:
                lead = Lead(
                    user_id=owner_id,
                    source=LeadSource.CONSULTATION.value,
                    status=LeadStatus.NEW.value,
                    priority=LeadPriority.NORMAL.value,
                    name=f"{payload.first_name} {payload.last_name}",
                    email=email,
                    phone=payload.phone,
                    location=payload.city,
                    project_summary=payload.message,
                )
                self.session.add(lead)
            else:
                lead.name = f"{payload.first_name} {payload.last_name}"
                lead.location = payload.city
                lead.project_summary = payload.message
                if payload.phone:
                    lead.phone = payload.phone
                if lead.user_id is None and owner_id is not None:
                    lead.user_id = owner_id

            await self.session.flush()

            consultation = ConsultationRequest(
                user_id=owner_id,
                lead_id=lead.id,
                first_name=payload.first_name,
                last_name=payload.last_name,
                email=email,
                phone=payload.phone,
                project_type=payload.project_type.value,
                location=payload.city,
                message=payload.message,
                status=LeadStatus.NEW.value,
            )
            self.session.add(consultation)
            await self.session.flush()

            self.session.add(
                CommunicationEvent(
                    user_id=owner_id,
                    lead_id=lead.id,
                    event_type=CommunicationEventType.CONSULTATION_RECEIVED.value,
                    channel=ConversationChannel.WEB.value,
                    event_metadata={"consultation_id": str(consultation.id)},
                )
            )
            self.session.add(
                CommunicationEvent(
                    user_id=owner_id,
                    lead_id=lead.id,
                    event_type=(
                        CommunicationEventType.LEAD_CREATED.value
                        if created_lead
                        else CommunicationEventType.LEAD_UPDATED.value
                    ),
                    channel=ConversationChannel.WEB.value,
                    event_metadata={"consultation_id": str(consultation.id)},
                )
            )
            await self.session.commit()
        except AppError:
            await self.session.rollback()
            raise
        except Exception as exc:
            await self.session.rollback()
            logger.error(
                "Consultation submission failed",
                extra={"error_type": type(exc).__name__},
            )
            raise AppError("We couldn't save your consultation request. Please try again.") from None

        await self._record_email(payload, lead, consultation, owner_id)

        return ConsultationAccepted(
            consultation_id=consultation.id,
            lead_id=lead.id,
            status=LeadStatus.NEW,
            message=_CONFIRMATION,
        )

    async def _record_email(
        self,
        payload: ConsultationSubmission,
        lead: Lead,
        consultation: ConsultationRequest,
        owner_id: UUID | None,
    ) -> None:
        submitted_at = consultation.created_at
        if not isinstance(submitted_at, datetime):
            submitted_at = utc_now()
        notice = ConsultationEmailContext(
            name=f"{payload.first_name} {payload.last_name}",
            email=str(payload.email),
            phone=payload.phone,
            city=payload.city,
            project_type=payload.project_type.value,
            message=payload.message,
            consultation_id=str(consultation.id),
            lead_id=str(lead.id),
            submitted_at=submitted_at,
        )
        try:
            attempts = await self.email_service.deliver_consultation(notice)
            for attempt in attempts:
                self.session.add(self._email_event(lead, consultation, attempt, owner_id))
            if attempts:
                await self.session.commit()
        except Exception as exc:
            await self.session.rollback()
            logger.error(
                "Consultation email result was not recorded",
                extra={
                    "consultation_id": str(consultation.id),
                    "lead_id": str(lead.id),
                    "error_type": type(exc).__name__,
                },
            )

    def _email_event(
        self,
        lead: Lead,
        consultation: ConsultationRequest,
        attempt: EmailAttempt,
        owner_id: UUID | None,
    ) -> CommunicationEvent:
        metadata: dict[str, str] = {
            "purpose": attempt.purpose,
            "recipient": attempt.recipient,
            "consultation_id": str(consultation.id),
            "result": attempt.result,
        }
        if attempt.error_type:
            metadata["error_type"] = attempt.error_type
        return CommunicationEvent(
            user_id=owner_id,
            lead_id=lead.id,
            event_type=CommunicationEventType.EMAIL_SENT.value,
            channel=ConversationChannel.EMAIL.value,
            event_metadata=metadata,
        )

    async def list_for_user(self, user_id: UUID, *, page: int, page_size: int) -> ConsultationHistoryPage:
        """Return one customer's consultations, newest first.

        The caller must pass the id from the verified session. This query does
        not accept another user's id from the request.
        """

        total = await self.session.scalar(
            select(func.count())
            .select_from(ConsultationRequest)
            .where(ConsultationRequest.user_id == user_id)
        )
        total_count = int(total or 0)
        offset = (page - 1) * page_size
        result = await self.session.scalars(
            select(ConsultationRequest)
            .where(ConsultationRequest.user_id == user_id)
            .order_by(ConsultationRequest.created_at.desc(), ConsultationRequest.id.desc())
            .offset(offset)
            .limit(page_size)
        )
        rows = list(result.all())
        return ConsultationHistoryPage(
            items=[
                ConsultationHistoryItem(
                    id=row.id,
                    created_at=row.created_at,
                    project_type=row.project_type,
                    city=row.location,
                    status=row.status,
                    message=row.message,
                )
                for row in rows
            ],
            page=page,
            page_size=page_size,
            total=total_count,
            has_next=offset + len(rows) < total_count,
        )

    async def _open_lead(self, email: str) -> Lead | None:
        statement = (
            select(Lead)
            .where(func.lower(Lead.email) == email, Lead.status.notin_(_CLOSED))
            .order_by(Lead.created_at.desc())
            .limit(1)
        )
        found = await self.session.scalar(statement)
        return found if isinstance(found, Lead) else None
