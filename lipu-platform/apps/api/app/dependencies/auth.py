"""Request identity.

Account routes verify the Clerk session token. `get_current_user` remains the
anonymous context used by older call sites and does not accept a password or a
client-supplied user id.
"""

from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, Request

from app.core.config import get_settings
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.domain.identity import ClerkIdentity
from app.services.clerk_auth import verify_clerk_bearer


@dataclass(frozen=True)
class CurrentUser:
    user_id: UUID | None
    clerk_id: str | None
    organization_id: UUID | None
    roles: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()

    @property
    def is_authenticated(self) -> bool:
        return self.clerk_id is not None


async def get_current_user(request: Request) -> CurrentUser:
    """Return anonymous context unless an older caller already set request.state.user."""

    user = getattr(request.state, "user", None)
    if isinstance(user, CurrentUser):
        return user
    return CurrentUser(user_id=None, clerk_id=None, organization_id=None)


async def get_optional_clerk_identity(request: Request) -> ClerkIdentity | None:
    """Return the verified Clerk user, or None when the request is anonymous.

    A bearer token that Clerk cannot verify is rejected. It is never treated as
    a guest and never mapped from a user id in the body.
    """

    header = request.headers.get("authorization", "")
    if not header.lower().startswith("bearer "):
        return None
    settings = get_settings()
    return await verify_clerk_bearer(
        header,
        secret_key=settings.clerk_secret_key,
        authorized_parties=settings.clerk_authorized_parties,
    )


async def require_clerk_identity(
    identity: ClerkIdentity | None = Depends(get_optional_clerk_identity),
) -> ClerkIdentity:
    if identity is None:
        raise UnauthorizedError("Authentication is required.")
    return identity


async def require_staff_access(
    identity: ClerkIdentity = Depends(require_clerk_identity),
) -> ClerkIdentity:
    """Keep foundation staff routes closed until a staff role exists."""

    del identity
    raise ForbiddenError("This resource is not available.")

