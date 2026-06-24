"""Authentication dependency foundation.

Concrete Clerk JWT validation belongs in the authentication sprint. This module
defines the request user shape and a single dependency point for future routes.
"""

from dataclasses import dataclass
from uuid import UUID

from fastapi import Request


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
    """Return request user context.

    Sprint 0 intentionally does not validate Clerk tokens. Middleware or auth
    dependencies can later populate request.state.user from validated claims.
    """

    user = getattr(request.state, "user", None)
    if isinstance(user, CurrentUser):
        return user
    return CurrentUser(user_id=None, clerk_id=None, organization_id=None)

