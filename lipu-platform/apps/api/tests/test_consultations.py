"""Consultation capture against an in-memory session double."""

from collections.abc import AsyncIterator
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.api.v1.consultations import get_session
from app.domain.enums import CommunicationEventType, LeadPriority, LeadSource, LeadStatus
from app.main import app
from app.models.communication import CommunicationEvent
from app.models.consultation_request import ConsultationRequest
from app.models.lead import Lead


class MemorySession:
    """Records objects the consultation service would persist."""

    def __init__(self, fail_commit: bool = False) -> None:
        self.leads: list[Lead] = []
        self.consultations: list[ConsultationRequest] = []
        self.events: list[CommunicationEvent] = []
        self.fail_commit = fail_commit
        self.committed = False
        self.rolled_back = False

    def add(self, obj: object) -> None:
        if isinstance(obj, Lead):
            self.leads.append(obj)
        elif isinstance(obj, ConsultationRequest):
            self.consultations.append(obj)
        elif isinstance(obj, CommunicationEvent):
            self.events.append(obj)

    async def flush(self) -> None:
        for collection in (self.leads, self.consultations, self.events):
            for obj in collection:
                if getattr(obj, "id", None) is None:
                    obj.id = uuid4()

    async def commit(self) -> None:
        if self.fail_commit:
            raise RuntimeError("database unavailable")
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True
        if not self.committed:
            self.leads.clear()
            self.consultations.clear()
            self.events.clear()

    async def scalar(self, statement: object) -> Lead | None:
        del statement
        open_leads = [lead for lead in self.leads if lead.status not in {"WON", "LOST", "CLOSED"}]
        return open_leads[-1] if open_leads else None

    async def refresh(self, obj: object) -> None:
        del obj


@pytest.fixture
def memory_session() -> MemorySession:
    session = MemorySession()

    async def override() -> AsyncIterator[MemorySession]:
        yield session

    app.dependency_overrides[get_session] = override
    yield session
    app.dependency_overrides.clear()


def _payload(**overrides: object) -> dict[str, object]:
    body: dict[str, object] = {
        "first_name": "Asha",
        "last_name": "Rao",
        "email": "Asha@Example.com",
        "phone": "+91 98765 43210",
        "city": "Bhubaneswar",
        "project_type": "residential",
        "message": "We want larger openings in the living room.",
    }
    body.update(overrides)
    return body


@pytest.mark.asyncio
async def test_guest_consultation_creates_lead_and_request(memory_session: MemorySession) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        response = await client.post("/api/v1/consultations", json=_payload())

    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["status"] == "NEW"
    assert body["message"] == "Your consultation request has been received."
    assert "traceback" not in response.text.lower()

    assert len(memory_session.leads) == 1
    lead = memory_session.leads[0]
    assert lead.source == LeadSource.CONSULTATION.value
    assert lead.status == LeadStatus.NEW.value
    assert lead.priority == LeadPriority.NORMAL.value
    assert lead.email == "asha@example.com"
    assert lead.user_id is None
    assert lead.phone == "+91 98765 43210"
    assert lead.location == "Bhubaneswar"

    assert len(memory_session.consultations) == 1
    consultation = memory_session.consultations[0]
    assert consultation.lead_id == lead.id
    assert consultation.user_id is None
    assert consultation.status == LeadStatus.NEW.value
    assert consultation.project_type == "RESIDENTIAL"
    assert str(consultation.id) == body["consultation_id"]
    assert str(lead.id) == body["lead_id"]

    event_types = {event.event_type for event in memory_session.events}
    assert CommunicationEventType.CONSULTATION_RECEIVED.value in event_types
    assert CommunicationEventType.LEAD_CREATED.value in event_types
    assert memory_session.committed is True


@pytest.mark.asyncio
async def test_consultation_succeeds_without_phone(memory_session: MemorySession) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        response = await client.post("/api/v1/consultations", json=_payload(phone=None))

    assert response.status_code == 201
    assert memory_session.consultations[0].phone is None
    assert memory_session.leads[0].phone is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "overrides",
    [
        {"email": "not-an-email"},
        {"project_type": "FACTORY"},
        {"first_name": " "},
        {"message": ""},
    ],
)
async def test_consultation_rejects_invalid_payload(
    memory_session: MemorySession, overrides: dict[str, str]
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        response = await client.post("/api/v1/consultations", json=_payload(**overrides))

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"
    assert memory_session.leads == []
    assert memory_session.consultations == []


@pytest.mark.asyncio
async def test_consultation_rolls_back_when_commit_fails() -> None:
    session = MemorySession(fail_commit=True)

    async def override() -> AsyncIterator[MemorySession]:
        yield session

    app.dependency_overrides[get_session] = override
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://localhost") as client:
            response = await client.post("/api/v1/consultations", json=_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    message = response.json()["error"]["message"]
    assert "Internal Server Error" not in message
    assert "sql" not in message.lower()
    assert session.committed is False
    assert session.rolled_back is True
    assert session.leads == []
    assert session.consultations == []
    assert session.events == []


@pytest.mark.asyncio
async def test_repeat_email_reuses_the_open_lead(memory_session: MemorySession) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        first = await client.post("/api/v1/consultations", json=_payload())
        second = await client.post(
            "/api/v1/consultations",
            json=_payload(message="A second note about the same home.", project_type="renovation"),
        )

    assert first.status_code == 201
    assert second.status_code == 201
    assert first.json()["lead_id"] == second.json()["lead_id"]
    assert first.json()["consultation_id"] != second.json()["consultation_id"]
    assert len(memory_session.leads) == 1
    assert len(memory_session.consultations) == 2
    assert memory_session.consultations[0].lead_id == memory_session.consultations[1].lead_id
    assert memory_session.leads[0].status == LeadStatus.NEW.value
    assert memory_session.consultations[1].project_type == "RENOVATION"
    updated = [
        event
        for event in memory_session.events
        if event.event_type == CommunicationEventType.LEAD_UPDATED.value
    ]
    assert len(updated) == 1


@pytest.mark.asyncio
async def test_guest_consultation_ignores_a_supplied_user_id(memory_session: MemorySession) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        response = await client.post("/api/v1/consultations", json=_payload(user_id=str(uuid4())))

    assert response.status_code == 201
    assert memory_session.leads[0].user_id is None
    assert memory_session.consultations[0].user_id is None
    assert all(event.user_id is None for event in memory_session.events)


@pytest.mark.asyncio
async def test_authenticated_consultation_stores_the_session_user(memory_session: MemorySession) -> None:
    from app.dependencies.account import get_account_service
    from app.dependencies.auth import get_optional_clerk_identity
    from app.domain.identity import ClerkIdentity

    owner_id = uuid4()
    identity = ClerkIdentity(
        clerk_id="user_session",
        email="asha@example.com",
        first_name="Asha",
        last_name="Rao",
        avatar_url=None,
    )

    class Accounts:
        async def sync_identity(self, current: ClerkIdentity) -> object:
            assert current.clerk_id == "user_session"
            return type("Owner", (), {"id": owner_id})()

    async def current_identity() -> ClerkIdentity:
        return identity

    app.dependency_overrides[get_optional_clerk_identity] = current_identity
    app.dependency_overrides[get_account_service] = lambda: Accounts()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        response = await client.post(
            "/api/v1/consultations",
            json=_payload(user_id=str(uuid4())),
        )

    assert response.status_code == 201
    assert memory_session.leads[0].user_id == owner_id
    assert memory_session.consultations[0].user_id == owner_id
    assert all(event.user_id == owner_id for event in memory_session.events)


@pytest.mark.asyncio
async def test_consultation_rejects_an_unverified_bearer_token(memory_session: MemorySession) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost") as client:
        response = await client.post(
            "/api/v1/consultations",
            json=_payload(),
            headers={"Authorization": "Bearer not-a-clerk-session"},
        )

    assert response.status_code == 401
    assert memory_session.leads == []
    assert memory_session.consultations == []
