"""Read-only consultation history for the signed-in customer."""

from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select

from app.db.session import AsyncSessionLocal, engine
from app.dependencies.auth import get_optional_clerk_identity
from app.domain.identity import ClerkIdentity
from app.main import app
from app.models.communication import CommunicationEvent
from app.models.consultation_request import ConsultationRequest
from app.models.lead import Lead
from app.models.user import User
from app.models.user_profile import UserProfile


async def _purge(clerk_id: str, email: str) -> None:
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(User).where(User.clerk_id == clerk_id))
        user_id = user.id if user is not None else None
        lead_ids = set((await session.scalars(select(Lead.id).where(Lead.email == email))).all())
        if user_id is not None:
            owned = (await session.scalars(select(Lead.id).where(Lead.user_id == user_id))).all()
            lead_ids.update(owned)
        if lead_ids:
            await session.execute(delete(CommunicationEvent).where(CommunicationEvent.lead_id.in_(lead_ids)))
            await session.execute(delete(ConsultationRequest).where(ConsultationRequest.lead_id.in_(lead_ids)))
            await session.execute(delete(Lead).where(Lead.id.in_(lead_ids)))
        if user_id is not None:
            await session.execute(delete(CommunicationEvent).where(CommunicationEvent.user_id == user_id))
            await session.execute(delete(ConsultationRequest).where(ConsultationRequest.user_id == user_id))
            await session.execute(delete(UserProfile).where(UserProfile.user_id == user_id))
            await session.execute(delete(User).where(User.id == user_id))
        await session.commit()


def _identity(name: str) -> ClerkIdentity:
    return ClerkIdentity(
        clerk_id=f"test_clerk_{uuid4().hex}",
        email=f"history-{name}-{uuid4().hex}@example.com",
        first_name=name,
        last_name="Rao",
        avatar_url=None,
    )


def _use(identity: ClerkIdentity) -> None:
    async def current() -> ClerkIdentity:
        return identity

    app.dependency_overrides[get_optional_clerk_identity] = current


def _client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")


def _body(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "first_name": "Asha",
        "last_name": "Rao",
        "email": "asha@example.com",
        "phone": None,
        "city": "Bhubaneswar",
        "project_type": "residential",
        "message": "We want larger openings in the living room.",
    }
    payload.update(overrides)
    return payload


async def _stamp(consultation_id: str, when: datetime) -> None:
    async with AsyncSessionLocal() as session:
        row = await session.get(ConsultationRequest, UUID(consultation_id))
        assert row is not None
        row.created_at = when
        await session.commit()


@pytest_asyncio.fixture
async def identities() -> AsyncIterator[tuple[ClerkIdentity, ClerkIdentity]]:
    owner = _identity("Asha")
    other = _identity("Meera")
    try:
        yield owner, other
    finally:
        app.dependency_overrides.pop(get_optional_clerk_identity, None)
        await _purge(owner.clerk_id, owner.email)
        await _purge(other.clerk_id, other.email)
        await engine.dispose()


@pytest.mark.asyncio
async def test_consultation_history_requires_authentication() -> None:
    app.dependency_overrides.pop(get_optional_clerk_identity, None)
    async with _client() as client:
        response = await client.get("/api/v1/consultations/me")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


@pytest.mark.asyncio
async def test_consultation_history_is_empty_for_a_new_account(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        response = await client.get("/api/v1/consultations/me")

    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["page"] == 1
    assert body["page_size"] == 10
    assert body["total"] == 0
    assert body["has_next"] is False


@pytest.mark.asyncio
async def test_consultation_history_returns_only_the_signed_in_user(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, other = identities
    _use(owner)
    async with _client() as client:
        mine = await client.post("/api/v1/consultations", json=_body(email=owner.email, city="Bhubaneswar"))
        _use(other)
        theirs = await client.post(
            "/api/v1/consultations",
            json=_body(
                email=other.email,
                first_name="Meera",
                city="Cuttack",
                project_type="commercial",
                message="Showroom glazing for another account.",
            ),
        )
        _use(owner)
        response = await client.get(f"/api/v1/consultations/me?user_id={theirs.json()['consultation_id']}")

    assert mine.status_code == 201
    assert theirs.status_code == 201
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert len(body["items"]) == 1
    item = body["items"][0]
    assert item["id"] == mine.json()["consultation_id"]
    assert item["city"] == "Bhubaneswar"
    assert item["project_type"] == "RESIDENTIAL"
    assert item["status"] == "NEW"
    assert item["message"] == "We want larger openings in the living room."
    assert "lead_id" not in item
    assert "user_id" not in item
    assert "Showroom glazing" not in response.text


@pytest.mark.asyncio
async def test_consultation_history_pages_newest_first(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    created: list[str] = []
    async with _client() as client:
        for index, message in enumerate(("Oldest note.", "Middle note.", "Newest note.")):
            response = await client.post(
                "/api/v1/consultations",
                json=_body(email=owner.email, message=message, city=f"City {index}"),
            )
            assert response.status_code == 201
            created.append(response.json()["consultation_id"])

    base = datetime(2026, 9, 1, tzinfo=UTC)
    for index, consultation_id in enumerate(created):
        await _stamp(consultation_id, base + timedelta(days=index))

    async with _client() as client:
        first = await client.get("/api/v1/consultations/me?page=1&page_size=2")
        second = await client.get("/api/v1/consultations/me?page=2&page_size=2")

    assert first.status_code == 200
    page_one = first.json()
    assert page_one["total"] == 3
    assert page_one["page"] == 1
    assert page_one["page_size"] == 2
    assert page_one["has_next"] is True
    assert [item["message"] for item in page_one["items"]] == ["Newest note.", "Middle note."]

    page_two = second.json()
    assert page_two["page"] == 2
    assert page_two["has_next"] is False
    assert [item["message"] for item in page_two["items"]] == ["Oldest note."]
