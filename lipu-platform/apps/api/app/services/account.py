"""Synchronise a Clerk identity with the local user and profile.

Guest consultations stay unattached. A later account that uses the same email
does not claim those historical leads or consultations. Linking a guest history
to a new account is a future feature and must be an explicit, reviewed action.
"""

from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppError
from app.domain.enums import ProjectType
from app.domain.identity import ClerkIdentity
from app.models.organization import Organization
from app.models.user import User
from app.models.user_profile import UserProfile
from app.repositories.organization import OrganizationRepository
from app.repositories.user import UserRepository
from app.schemas.account import MeRead, ProfileRead, ProfileUpdate
from app.services.base import BaseService


ECOTECH_ORGANIZATION_SLUG = "ecotech"
CUSTOMER_ROLE = "customer"


def _display_name(first_name: str | None, last_name: str | None) -> str | None:
    parts = [part for part in (first_name, last_name) if part]
    if not parts:
        return None
    return " ".join(parts)[:160]


def present_account(user: User) -> MeRead:
    profile = user.user_profile
    interests = list(profile.project_interests) if profile is not None else []
    return MeRead(
        id=user.id,
        clerk_id=user.clerk_id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        avatar_url=user.avatar_url,
        role=user.role,
        created_at=user.created_at,
        profile=ProfileRead(
            display_name=profile.display_name if profile is not None else None,
            preferred_contact_method=profile.preferred_contact_method if profile is not None else None,
            city=profile.city if profile is not None else None,
            state=profile.state if profile is not None else None,
            company=profile.company if profile is not None else None,
            project_interests=[str(item) for item in interests],
        ),
    )


class AccountService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.users = UserRepository(session)
        self.organizations = OrganizationRepository(session)

    async def sync_identity(self, identity: ClerkIdentity) -> User:
        """Find the local user for this Clerk id, or create one customer.

        Repeating this call updates the login stamp and does not insert another
        user. It does not look up historical leads by email.
        """

        existing = await self.users.get_by_clerk_id(identity.clerk_id)
        if existing is not None:
            return await self._touch(existing, identity)

        try:
            await self._create(identity)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()

        reloaded = await self.users.get_by_clerk_id(identity.clerk_id)
        if reloaded is None:
            raise AppError("Could not create the account.")
        if reloaded.login_count == 0 or reloaded.last_login is None:
            return await self._touch(reloaded, identity)
        return reloaded

    async def update_profile(self, user: User, payload: ProfileUpdate) -> User:
        values = payload.model_dump(exclude_unset=True)
        for field in ("first_name", "last_name", "phone"):
            if field in values:
                setattr(user, field, values[field])

        profile = user.user_profile
        if profile is None:
            profile = UserProfile(user_id=user.id, project_interests=[])
            self.session.add(profile)
            user.user_profile = profile

        if "city" in values:
            profile.city = values["city"]
        if "state" in values:
            profile.state = values["state"]
        if "company" in values:
            profile.company = values["company"]
        if "preferred_contact_method" in values:
            method = values["preferred_contact_method"]
            profile.preferred_contact_method = method.value if method is not None else None
        if "project_interests" in values:
            interests = values["project_interests"] or []
            profile.project_interests = [
                item.value if isinstance(item, ProjectType) else str(item) for item in interests
            ]
        if "first_name" in values or "last_name" in values or profile.display_name is None:
            profile.display_name = _display_name(user.first_name, user.last_name)

        await self.session.commit()
        reloaded = await self.users.get_by_clerk_id(user.clerk_id)
        if reloaded is None:
            raise AppError("Could not load the account.")
        return reloaded

    async def _organization(self) -> Organization:
        existing = await self.organizations.get_by_slug(ECOTECH_ORGANIZATION_SLUG)
        if existing is not None:
            return existing
        organization = Organization(
            name="Ecotech Window Systems",
            slug=ECOTECH_ORGANIZATION_SLUG,
            status="active",
        )
        self.session.add(organization)
        try:
            await self.session.flush()
        except IntegrityError:
            await self.session.rollback()
            existing = await self.organizations.get_by_slug(ECOTECH_ORGANIZATION_SLUG)
            if existing is None:
                raise
            return existing
        return organization

    async def _create(self, identity: ClerkIdentity) -> User:
        organization = await self._organization()
        now = datetime.now(UTC)
        user = User(
            clerk_id=identity.clerk_id,
            organization_id=organization.id,
            email=identity.email,
            first_name=identity.first_name,
            last_name=identity.last_name,
            avatar_url=identity.avatar_url,
            role=CUSTOMER_ROLE,
            permissions=[],
            profile={},
            password_hash=None,
            last_login=now,
            login_count=1,
            status="active",
        )
        self.session.add(user)
        await self.session.flush()
        profile = UserProfile(
            user_id=user.id,
            display_name=_display_name(identity.first_name, identity.last_name),
            project_interests=[],
        )
        self.session.add(profile)
        user.user_profile = profile
        return user

    async def _touch(self, user: User, identity: ClerkIdentity) -> User:
        user.email = identity.email
        if identity.avatar_url:
            user.avatar_url = identity.avatar_url
        if identity.first_name and not user.first_name:
            user.first_name = identity.first_name
        if identity.last_name and not user.last_name:
            user.last_name = identity.last_name
        user.last_login = datetime.now(UTC)
        user.login_count = (user.login_count or 0) + 1
        if user.user_profile is None:
            profile = UserProfile(
                user_id=user.id,
                display_name=_display_name(user.first_name, user.last_name),
                project_interests=[],
            )
            self.session.add(profile)
            user.user_profile = profile
        await self.session.commit()
        reloaded = await self.users.get_by_clerk_id(user.clerk_id)
        if reloaded is None:
            raise AppError("Could not load the account.")
        return reloaded
