"""Provider-agnostic consultation email delivery."""

import asyncio
import smtplib
from dataclasses import dataclass
from datetime import UTC, datetime
from email.message import EmailMessage
from email.utils import formataddr
from typing import Protocol

from app.core.config import Settings, get_settings
from app.core.logging import get_logger
from app.services.email_templates import (
    RenderedEmail,
    customer_acknowledgement,
    internal_notification,
)


logger = get_logger(__name__)


class EmailDeliveryError(Exception):
    """The message was not handed to the provider."""


class EmailProvider(Protocol):
    async def send(self, message: RenderedEmail) -> None:
        """Deliver one message. Raise EmailDeliveryError when it does not send."""


@dataclass(frozen=True)
class EmailAttempt:
    purpose: str
    recipient: str
    result: str
    error_type: str | None = None


@dataclass(frozen=True)
class ConsultationEmailContext:
    name: str
    email: str
    phone: str | None
    city: str
    project_type: str
    message: str
    consultation_id: str
    lead_id: str
    submitted_at: datetime


class SmtpEmailProvider:
    """Stdlib SMTP adapter. Domain code depends on EmailProvider, not this class."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def send(self, message: RenderedEmail) -> None:
        await asyncio.to_thread(self._send_sync, message)

    def _send_sync(self, message: RenderedEmail) -> None:
        settings = self._settings
        if not settings.email_smtp_host or not settings.email_from:
            raise EmailDeliveryError("Email provider is not configured.")
        payload = EmailMessage()
        payload["From"] = formataddr((settings.email_from_name, settings.email_from))
        payload["To"] = message.recipient
        payload["Subject"] = message.subject
        payload.set_content(message.text)
        payload.add_alternative(message.html, subtype="html")
        with smtplib.SMTP(settings.email_smtp_host, settings.email_smtp_port, timeout=15) as smtp:
            if settings.email_smtp_use_tls:
                smtp.starttls()
            if settings.email_smtp_username:
                smtp.login(settings.email_smtp_username, settings.email_smtp_password)
            smtp.send_message(payload)


class EmailService:
    def __init__(self, settings: Settings, provider: EmailProvider) -> None:
        self._settings = settings
        self._provider = provider

    async def deliver_consultation(self, notice: ConsultationEmailContext) -> list[EmailAttempt]:
        if not self._settings.email_enabled:
            logger.info(
                "Consultation email disabled",
                extra={
                    "consultation_id": notice.consultation_id,
                    "lead_id": notice.lead_id,
                },
            )
            return []

        messages = [
            internal_notification(
                recipient=self._settings.ecotech_notification_email,
                name=notice.name,
                email=notice.email,
                phone=notice.phone,
                city=notice.city,
                project_type=notice.project_type,
                message=notice.message,
                consultation_id=notice.consultation_id,
                lead_id=notice.lead_id,
                submitted_at=notice.submitted_at,
            ),
            customer_acknowledgement(
                recipient=notice.email,
                name=notice.name,
                city=notice.city,
                project_type=notice.project_type,
                message=notice.message,
                consultation_id=notice.consultation_id,
            ),
        ]
        attempts: list[EmailAttempt] = []
        for message in messages:
            attempts.append(await self._send_one(notice, message))
        return attempts

    async def _send_one(self, notice: ConsultationEmailContext, message: RenderedEmail) -> EmailAttempt:
        if not message.recipient or "@" not in message.recipient:
            return self._failed(notice, message, "MissingRecipient")
        try:
            await self._provider.send(message)
        except Exception as exc:
            return self._failed(notice, message, type(exc).__name__)
        logger.info(
            "Consultation email sent",
            extra={
                "consultation_id": notice.consultation_id,
                "lead_id": notice.lead_id,
                "purpose": message.purpose,
                "recipient_domain": _domain(message.recipient),
                "result": "sent",
            },
        )
        return EmailAttempt(purpose=message.purpose, recipient=message.recipient, result="sent")

    def _failed(
        self, notice: ConsultationEmailContext, message: RenderedEmail, error_type: str
    ) -> EmailAttempt:
        logger.error(
            "Consultation email failed",
            extra={
                "consultation_id": notice.consultation_id,
                "lead_id": notice.lead_id,
                "purpose": message.purpose,
                "recipient_domain": _domain(message.recipient),
                "result": "failed",
                "error_type": error_type,
            },
        )
        return EmailAttempt(
            purpose=message.purpose,
            recipient=message.recipient,
            result="failed",
            error_type=error_type,
        )


def build_email_service(settings: Settings | None = None) -> EmailService:
    selected = settings or get_settings()
    return EmailService(selected, SmtpEmailProvider(selected))


def _domain(recipient: str) -> str:
    if "@" not in recipient:
        return "unknown"
    return recipient.rsplit("@", 1)[-1]


def utc_now() -> datetime:
    return datetime.now(UTC)
