"""Read-only transform history for the signed-in customer."""

from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select

from app.db.session import AsyncSessionLocal, engine
from app.dependencies.auth import get_optional_clerk_identity
from app.domain.enums import TransformStatus
from app.domain.identity import ClerkIdentity
from app.main import app
from app.models.transform import TransformAsset, TransformRequest, TransformResult
from app.models.user import User
from app.models.user_profile import UserProfile


async def _purge(clerk_id: str) -> None:
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(User).where(User.clerk_id == clerk_id))
        if user is not None:
            request_ids = list(
                (
                    await session.scalars(
                        select(TransformRequest.id).where(TransformRequest.user_id == user.id)
                    )
                ).all()
            )
            if request_ids:
                await session.execute(
                    delete(TransformResult).where(TransformResult.transform_request_id.in_(request_ids))
                )
                await session.execute(
                    delete(TransformAsset).where(TransformAsset.transform_request_id.in_(request_ids))
                )
                await session.execute(delete(TransformRequest).where(TransformRequest.id.in_(request_ids)))
            await session.execute(delete(UserProfile).where(UserProfile.user_id == user.id))
            await session.execute(delete(User).where(User.id == user.id))
        await session.commit()


def _identity(name: str) -> ClerkIdentity:
    return ClerkIdentity(
        clerk_id=f"test_clerk_{uuid4().hex}",
        email=f"transform-{name}-{uuid4().hex}@example.com",
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


async def _user_id(clerk_id: str) -> UUID:
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(User).where(User.clerk_id == clerk_id))
        assert user is not None
        return user.id


async def _add_request(
    user_id: UUID,
    *,
    target: str,
    variant: str | None,
    status: str,
    source_key: str | None = None,
    result_key: str | None = None,
    with_result: bool = False,
) -> UUID:
    async with AsyncSessionLocal() as session:
        request = TransformRequest(user_id=user_id, target=target, variant=variant, status=status)
        session.add(request)
        await session.flush()
        if source_key is not None:
            session.add(
                TransformAsset(
                    transform_request_id=request.id,
                    asset_type="SOURCE",
                    storage_key=source_key,
                    mime_type="image/png",
                    asset_metadata={"note": "staff-only-note"},
                )
            )
        result_asset_id = None
        if result_key is not None:
            result_asset = TransformAsset(
                transform_request_id=request.id,
                asset_type="RESULT",
                storage_key=result_key,
                mime_type="image/png",
                asset_metadata={},
            )
            session.add(result_asset)
            await session.flush()
            result_asset_id = result_asset.id
        if with_result or result_key is not None:
            session.add(
                TransformResult(
                    transform_request_id=request.id,
                    result_asset_id=result_asset_id,
                )
            )
        await session.commit()
        return request.id


async def _stamp(request_id: UUID, when: datetime) -> None:
    async with AsyncSessionLocal() as session:
        row = await session.get(TransformRequest, request_id)
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
        await _purge(owner.clerk_id)
        await _purge(other.clerk_id)
        await engine.dispose()


@pytest.mark.asyncio
async def test_transform_history_requires_authentication() -> None:
    app.dependency_overrides.pop(get_optional_clerk_identity, None)
    async with _client() as client:
        response = await client.get("/api/v1/transform/requests/me")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


@pytest.mark.asyncio
async def test_transform_history_rejects_an_invalid_session() -> None:
    app.dependency_overrides.pop(get_optional_clerk_identity, None)
    async with _client() as client:
        response = await client.get(
            "/api/v1/transform/requests/me",
            headers={"Authorization": "Bearer not-a-session"},
        )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


@pytest.mark.asyncio
async def test_transform_history_is_empty_for_a_new_account(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        response = await client.get("/api/v1/transform/requests/me")

    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["page"] == 1
    assert body["page_size"] == 10
    assert body["total"] == 0
    assert body["has_next"] is False


@pytest.mark.asyncio
async def test_transform_history_returns_only_the_signed_in_user(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, other = identities
    _use(owner)
    async with _client() as client:
        await client.get("/api/v1/users/me")
        _use(other)
        await client.get("/api/v1/users/me")
    owner_id = await _user_id(owner.clerk_id)
    other_id = await _user_id(other.clerk_id)
    mine = await _add_request(owner_id, target="WINDOWS", variant="SLIDING", status="COMPLETED")
    theirs = await _add_request(other_id, target="DOORS", variant="FRENCH", status="UPLOADED")

    _use(owner)
    async with _client() as client:
        response = await client.get(f"/api/v1/transform/requests/me?user_id={other_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert [item["id"] for item in body["items"]] == [str(mine)]
    assert body["items"][0]["target"] == "WINDOWS"
    assert str(theirs) not in response.text
    assert "DOORS" not in response.text
    assert "user_id" not in body["items"][0]
    assert "lead_id" not in body["items"][0]


@pytest.mark.asyncio
async def test_transform_history_pages_newest_first(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        await client.get("/api/v1/users/me")
    owner_id = await _user_id(owner.clerk_id)
    created = []
    for target in ("WINDOWS", "DOORS", "BALCONY"):
        created.append(
            await _add_request(owner_id, target=target, variant=None, status="CONFIGURED")
        )
    base = datetime(2026, 9, 1, tzinfo=UTC)
    for index, request_id in enumerate(created):
        await _stamp(request_id, base + timedelta(days=index))

    async with _client() as client:
        first = await client.get("/api/v1/transform/requests/me?page=1&page_size=2")
        second = await client.get("/api/v1/transform/requests/me?page=2&page_size=2")

    assert first.status_code == 200
    page_one = first.json()
    assert page_one["total"] == 3
    assert page_one["page"] == 1
    assert page_one["page_size"] == 2
    assert page_one["has_next"] is True
    assert [item["target"] for item in page_one["items"]] == ["BALCONY", "DOORS"]
    page_two = second.json()
    assert page_two["page"] == 2
    assert page_two["has_next"] is False
    assert [item["target"] for item in page_two["items"]] == ["WINDOWS"]
    assert page_two["items"][0]["variant"] is None


@pytest.mark.asyncio
async def test_transform_history_returns_a_result_without_internal_storage(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        await client.get("/api/v1/users/me")
    owner_id = await _user_id(owner.clerk_id)
    public = "/images/transform/ecotech/transform-sample-living-01.png"
    private = "private/secret-object-key"
    await _add_request(
        owner_id,
        target="TERRACE",
        variant="LARGE_OPENING",
        status="COMPLETED",
        source_key=private,
        result_key=public,
        with_result=True,
    )

    async with _client() as client:
        response = await client.get("/api/v1/transform/requests/me")

    assert response.status_code == 200
    item = response.json()["items"][0]
    assert item["status"] == "COMPLETED"
    assert item["variant"] == "LARGE_OPENING"
    assert item["source_asset"]["public_url"] is None
    assert item["source_asset"]["mime_type"] == "image/png"
    assert item["result"]["asset"]["public_url"] == public
    assert "storage_key" not in response.text
    assert private not in response.text
    assert "staff-only-note" not in response.text
    assert "lead_id" not in item
    assert "user_id" not in item


@pytest.mark.asyncio
async def test_transform_history_allows_a_request_without_result_or_variant(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        await client.get("/api/v1/users/me")
    owner_id = await _user_id(owner.clerk_id)
    await _add_request(owner_id, target="OUTDOOR", variant=None, status="UPLOADED")

    async with _client() as client:
        response = await client.get("/api/v1/transform/requests/me")

    assert response.status_code == 200
    item = response.json()["items"][0]
    assert item["variant"] is None
    assert item["source_asset"] is None
    assert item["result"] is None
    assert item["status"] == "UPLOADED"


@pytest.mark.asyncio
async def test_transform_history_serializes_every_status(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        await client.get("/api/v1/users/me")
    owner_id = await _user_id(owner.clerk_id)
    for status in TransformStatus:
        await _add_request(owner_id, target="WINDOWS", variant="CASEMENT", status=status.value)

    async with _client() as client:
        response = await client.get("/api/v1/transform/requests/me?page_size=10")

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == len(TransformStatus)
    assert {item["status"] for item in body["items"]} == {status.value for status in TransformStatus}
    assert {item["target"] for item in body["items"]} == {"WINDOWS"}
    assert {item["variant"] for item in body["items"]} == {"CASEMENT"}
