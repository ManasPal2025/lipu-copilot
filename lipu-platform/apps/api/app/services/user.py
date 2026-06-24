"""User application service."""

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.user import User
from app.repositories.organization import OrganizationRepository
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.services.base import BaseService


class UserService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.users = UserRepository(session)
        self.organizations = OrganizationRepository(session)

    async def list_users(
        self,
        *,
        organization_id: UUID | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> list[User]:
        return list(await self.users.list_active(organization_id=organization_id, offset=offset, limit=limit))

    async def get_user(self, user_id: UUID) -> User:
        user = await self.users.get_active(user_id)
        if user is None:
            raise NotFoundError("User not found.")
        return user

    async def create_user(self, payload: UserCreate) -> User:
        await self._ensure_organization_exists(payload.organization_id)
        if await self.users.get_by_clerk_id(payload.clerk_id):
            raise ConflictError("Clerk ID already exists.", details={"clerk_id": payload.clerk_id})
        if await self.users.get_by_email(str(payload.email)):
            raise ConflictError("User email already exists.", details={"email": str(payload.email)})

        values = payload.model_dump()
        values["email"] = str(values["email"])
        user = await self.users.create(**values)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_user(self, user_id: UUID, payload: UserUpdate) -> User:
        user = await self.get_user(user_id)
        values = payload.model_dump(exclude_unset=True)

        if "organization_id" in values:
            await self._ensure_organization_exists(values["organization_id"])

        if "email" in values:
            values["email"] = str(values["email"])
            existing = await self.users.get_by_email(values["email"])
            if existing and existing.id != user_id:
                raise ConflictError("User email already exists.", details={"email": values["email"]})

        updated = await self.users.update(user, **values)
        await self.session.commit()
        await self.session.refresh(updated)
        return updated

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.get_user(user_id)
        user.deleted_at = datetime.now(UTC)
        await self.session.commit()

    async def _ensure_organization_exists(self, organization_id: UUID) -> None:
        organization = await self.organizations.get_active(organization_id)
        if organization is None:
            raise NotFoundError("Organization not found.", details={"organization_id": str(organization_id)})

