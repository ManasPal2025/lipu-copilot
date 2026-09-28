"""Account sync and /users/me against PostgreSQL.

Rows created here are removed before the test process exits.
"""

from collections.abc import AsyncIterator
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, func, select

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
            await session.execute(
                delete(ConsultationRequest).where(ConsultationRequest.lead_id.in_(lead_ids))
            )
            await session.execute(delete(Lead).where(Lead.id.in_(lead_ids)))
        if user_id is not None:
            await session.execute(delete(CommunicationEvent).where(CommunicationEvent.user_id == user_id))
            await session.execute(
                delete(ConsultationRequest).where(ConsultationRequest.user_id == user_id)
            )
            await session.execute(delete(UserProfile).where(UserProfile.user_id == user_id))
            await session.execute(delete(User).where(User.id == user_id))
        await session.commit()


@pytest_asyncio.fixture
async def identity() -> AsyncIterator[ClerkIdentity]:
    created = ClerkIdentity(
        clerk_id=f"test_clerk_{uuid4().hex}",
        email=f"auth-test-{uuid4().hex}@example.com",
        first_name="Asha",
        last_name="Rao",
        avatar_url=None,
    )

    async def current() -> ClerkIdentity:
        return created

    app.dependency_overrides[get_optional_clerk_identity] = current
    try:
        yield created
    finally:
        app.dependency_overrides.pop(get_optional_clerk_identity, None)
        await _purge(created.clerk_id, created.email)
        await engine.dispose()


def _client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")


@pytest.mark.asyncio
async def test_me_requires_authentication() -> None:
    app.dependency_overrides.pop(get_optional_clerk_identity, None)
    async with _client() as client:
        response = await client.get("/api/v1/users/me")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


@pytest.mark.asyncio
async def test_first_sync_creates_a_customer_and_repeat_sync_does_not_duplicate(
    identity: ClerkIdentity,
) -> None:
    async with _client() as client:
        first = await client.get("/api/v1/users/me")
        second = await client.get("/api/v1/users/me")

    assert first.status_code == 200
    assert second.status_code == 200
    body = first.json()
    assert body["id"] == second.json()["id"]
    assert body["clerk_id"] == identity.clerk_id
    assert body["email"] == identity.email
    assert body["role"] == "customer"
    assert body["first_name"] == "Asha"
    assert body["profile"]["display_name"] == "Asha Rao"
    assert "password" not in body
    assert "password_hash" not in body

    async with AsyncSessionLocal() as session:
        count = await session.scalar(
            select(func.count()).select_from(User).where(User.clerk_id == identity.clerk_id)
        )
        stored = await session.scalar(select(User).where(User.clerk_id == identity.clerk_id))
    assert count == 1
    assert stored is not None
    assert stored.password_hash is None
    assert stored.role == "customer"
    assert stored.login_count == 2


@pytest.mark.asyncio
async def test_profile_update_persists_and_ignores_role(identity: ClerkIdentity) -> None:
    async with _client() as client:
        response = await client.patch(
            "/api/v1/users/me",
            json={
                "first_name": "Meera",
                "last_name": "Das",
                "phone": "+91 98765 43210",
                "city": "Puri",
                "state": "Odisha",
                "company": "Studio North",
                "preferred_contact_method": "EMAIL",
                "project_interests": ["RESIDENTIAL", "RESIDENTIAL"],
                "role": "admin",
                "clerk_id": "user_someone_else",
                "password": "secret",
                "password_hash": "hash",
            },
        )
        again = await client.get("/api/v1/users/me")

    assert response.status_code == 200
    body = response.json()
    assert body["role"] == "customer"
    assert body["clerk_id"] == identity.clerk_id
    assert body["email"] == identity.email
    assert body["first_name"] == "Meera"
    assert body["last_name"] == "Das"
    assert body["phone"] == "+91 98765 43210"
    assert body["profile"]["city"] == "Puri"
    assert body["profile"]["state"] == "Odisha"
    assert body["profile"]["company"] == "Studio North"
    assert body["profile"]["preferred_contact_method"] == "EMAIL"
    assert body["profile"]["project_interests"] == ["RESIDENTIAL"]
    assert "password_hash" not in body
    assert again.json()["profile"]["city"] == "Puri"
    assert again.json()["role"] == "customer"


@pytest.mark.asyncio
async def test_user_cannot_modify_another_user_or_their_role(identity: ClerkIdentity) -> None:
    async with _client() as client:
        me = await client.get("/api/v1/users/me")
        other = await client.patch(
            f"/api/v1/users/{uuid4()}",
            json={"first_name": "Other", "role": "admin"},
        )
        own_role = await client.patch(
            f"/api/v1/users/{me.json()['id']}",
            json={"role": "sales"},
        )
        current = await client.get("/api/v1/users/me")

    assert me.status_code == 200
    assert other.status_code == 403
    assert own_role.status_code == 403
    assert current.json()["role"] == "customer"
    assert current.json()["first_name"] == "Asha"
    assert current.json()["id"] == me.json()["id"]


@pytest.mark.asyncio
async def test_authenticated_consultation_stores_user_id(identity: ClerkIdentity) -> None:
    async with _client() as client:
        me = await client.get("/api/v1/users/me")
        created = await client.post(
            "/api/v1/consultations",
            json={
                "first_name": "Asha",
                "last_name": "Rao",
                "email": identity.email,
                "phone": None,
                "city": "Bhubaneswar",
                "project_type": "residential",
                "message": "A signed-in consultation for the living room.",
                "user_id": str(uuid4()),
            },
        )

    assert me.status_code == 200
    assert created.status_code == 201
    user_id = UUID(me.json()["id"])
    async with AsyncSessionLocal() as session:
        consultation = await session.get(ConsultationRequest, UUID(created.json()["consultation_id"]))
        lead = await session.get(Lead, UUID(created.json()["lead_id"]))
    assert consultation is not None
    assert lead is not None
    assert consultation.user_id == user_id
    assert lead.user_id == user_id
