"""Consultation email delivery against a fake provider."""

from collections.abc import AsyncIterator

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.v1.consultations import get_consultation_service, get_session
from app.core.config import get_settings
from app.core.exceptions import AppError
from app.domain.enums import CommunicationEventType
from app.main import app
from app.schemas.platform import ConsultationSubmission
from app.services.consultations import ConsultationService
from app.services.email import EmailService
from app.services.email_templates import RenderedEmail
from tests.test_consultations import MemorySession, _payload


STUDIO = "studio@example.com"


class FakeProvider:
    def __init__(self, fail_purposes: set[str] | None = None, fail_all: bool = False) -> None:
        self.sent: list[RenderedEmail] = []
        self.fail_purposes = fail_purposes or set()
        self.fail_all = fail_all

    async def send(self, message: RenderedEmail) -> None:
        if self.fail_all or message.purpose in self.fail_purposes:
            raise ConnectionError("provider unavailable")
        self.sent.append(message)


def _enabled_service(provider: FakeProvider) -> EmailService:
    settings = get_settings().model_copy(
        update={
            "email_enabled": True,
            "email_from": "notifications@example.com",
            "email_from_name": "Ecotech",
            "ecotech_notification_email": STUDIO,
        }
    )
    return EmailService(settings, provider)


def _submission(**overrides: object) -> ConsultationSubmission:
    return ConsultationSubmission.model_validate(_payload(**overrides))


def _email_events(session: MemorySession, purpose: str) -> list[dict[str, str]]:
    return [
        event.event_metadata
        for event in session.events
        if event.event_type == CommunicationEventType.EMAIL_SENT.value
        and event.event_metadata.get("purpose") == purpose
    ]


@pytest.mark.asyncio
async def test_successful_consultation_sends_both_emails() -> None:
    session = MemorySession()
    provider = FakeProvider()
    service = ConsultationService(session, _enabled_service(provider))

    result = await service.submit(_submission())

    assert result.success is True
    assert result.status.value == "NEW"
    assert len(session.leads) == 1
    assert len(session.consultations) == 1
    assert [message.purpose for message in provider.sent] == [
        "internal_notification",
        "customer_acknowledgement",
    ]
    internal, customer = provider.sent
    assert internal.recipient == STUDIO
    assert internal.subject == "New Consultation Request — Asha Rao"
    assert "asha@example.com" in internal.text
    assert "+91 98765 43210" in internal.text
    assert "Bhubaneswar" in internal.text
    assert "Residential" in internal.text
    assert str(result.consultation_id) in internal.text
    assert str(result.lead_id) in internal.text
    assert customer.recipient == "asha@example.com"
    assert customer.subject == "We received your Ecotech consultation request"
    assert "Thank you" in customer.text
    assert STUDIO not in customer.text
    assert "Lead ID" not in customer.text
    assert _email_events(session, "internal_notification")[0]["result"] == "sent"
    assert _email_events(session, "customer_acknowledgement")[0]["result"] == "sent"


@pytest.mark.asyncio
async def test_internal_email_failure_keeps_the_consultation() -> None:
    session = MemorySession()
    provider = FakeProvider(fail_purposes={"internal_notification"})
    service = ConsultationService(session, _enabled_service(provider))

    result = await service.submit(_submission())

    assert result.success is True
    assert len(session.leads) == 1
    assert len(session.consultations) == 1
    assert [message.purpose for message in provider.sent] == ["customer_acknowledgement"]
    assert _email_events(session, "internal_notification")[0]["result"] == "failed"
    assert _email_events(session, "customer_acknowledgement")[0]["result"] == "sent"


@pytest.mark.asyncio
async def test_customer_email_failure_does_not_mark_the_internal_notice_failed() -> None:
    session = MemorySession()
    provider = FakeProvider(fail_purposes={"customer_acknowledgement"})
    service = ConsultationService(session, _enabled_service(provider))

    result = await service.submit(_submission())

    assert result.success is True
    assert len(session.leads) == 1
    assert [message.purpose for message in provider.sent] == ["internal_notification"]
    assert _email_events(session, "internal_notification")[0]["result"] == "sent"
    customer = _email_events(session, "customer_acknowledgement")[0]
    assert customer["result"] == "failed"
    assert customer["error_type"] == "ConnectionError"
    assert "provider unavailable" not in str(customer)


@pytest.mark.asyncio
async def test_provider_unavailable_still_returns_success_without_secrets() -> None:
    session = MemorySession()
    provider = FakeProvider(fail_all=True)
    service = ConsultationService(session, _enabled_service(provider))

    result = await service.submit(_submission())

    assert result.message == "Your consultation request has been received."
    assert provider.sent == []
    assert len(session.leads) == 1
    assert len(session.consultations) == 1
    results = {item["purpose"]: item["result"] for item in _email_events(session, "internal_notification")}
    results.update(
        {item["purpose"]: item["result"] for item in _email_events(session, "customer_acknowledgement")}
    )
    assert results == {
        "internal_notification": "failed",
        "customer_acknowledgement": "failed",
    }
    stored = " ".join(str(event.event_metadata) for event in session.events)
    assert "lipu_password" not in stored
    assert "smtp" not in stored.lower()


@pytest.mark.asyncio
async def test_second_consultation_sends_a_separate_email_pair() -> None:
    session = MemorySession()
    provider = FakeProvider()
    service = ConsultationService(session, _enabled_service(provider))

    first = await service.submit(_submission())
    second = await service.submit(_submission(message="A second note about the same home."))

    assert first.lead_id == second.lead_id
    assert first.consultation_id != second.consultation_id
    assert len(session.leads) == 1
    assert len(session.consultations) == 2
    assert len(provider.sent) == 4
    assert [message.purpose for message in provider.sent] == [
        "internal_notification",
        "customer_acknowledgement",
        "internal_notification",
        "customer_acknowledgement",
    ]
    assert str(second.consultation_id) in provider.sent[2].text
    assert str(first.consultation_id) not in provider.sent[2].text


@pytest.mark.asyncio
async def test_missing_phone_is_omitted_from_the_internal_email() -> None:
    session = MemorySession()
    provider = FakeProvider()
    service = ConsultationService(session, _enabled_service(provider))

    await service.submit(_submission(phone=None))

    assert "Phone:" not in provider.sent[0].text
    assert "Phone" not in provider.sent[0].html
    assert session.consultations[0].phone is None


@pytest.mark.asyncio
async def test_database_failure_does_not_send_email() -> None:
    session = MemorySession(fail_commit=True)
    provider = FakeProvider()
    service = ConsultationService(session, _enabled_service(provider))

    with pytest.raises(AppError):
        await service.submit(_submission())

    assert provider.sent == []
    assert session.leads == []
    assert session.consultations == []
    assert session.events == []


@pytest.mark.asyncio
async def test_http_response_hides_email_failure() -> None:
    session = MemorySession()
    provider = FakeProvider(fail_all=True)

    def override_service() -> ConsultationService:
        return ConsultationService(session, _enabled_service(provider))

    async def override_session() -> AsyncIterator[MemorySession]:
        yield session

    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[get_consultation_service] = override_service
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://localhost") as client:
            response = await client.post("/api/v1/consultations", json=_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    body = response.json()
    assert set(body) == {"success", "consultation_id", "lead_id", "status", "message"}
    assert "provider" not in response.text.lower()
    assert "connectionerror" not in response.text.lower()
    assert STUDIO not in response.text
