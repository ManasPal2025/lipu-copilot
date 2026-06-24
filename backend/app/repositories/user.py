"""User repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_active(self, user_id: UUID) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id, User.deleted_at.is_(None)))
        return result.scalar_one_or_none()

    async def get_by_clerk_id(self, clerk_id: str) -> User | None:
        result = await self.session.execute(select(User).where(User.clerk_id == clerk_id, User.deleted_at.is_(None)))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email, User.deleted_at.is_(None)))
        return result.scalar_one_or_none()

    async def list_active(
        self,
        *,
        organization_id: UUID | None = None,
        offset: int = 0,
        limit: int = 100,
    ) -> Sequence[User]:
        query = select(User).where(User.deleted_at.is_(None)).order_by(User.created_at.desc())
        if organization_id is not None:
            query = query.where(User.organization_id == organization_id)
        result = await self.session.execute(query.offset(offset).limit(limit))
        return result.scalars().all()

