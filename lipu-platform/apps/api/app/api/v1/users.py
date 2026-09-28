"""Authenticated account routes.

`/users/me` is the public account API. Directory and role changes are not
available to signed-in customers. The local user is always taken from the
verified Clerk session, never from an id in the request.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.account import get_account_service
from app.dependencies.auth import require_clerk_identity
from app.dependencies.database import get_session
from app.domain.identity import ClerkIdentity
from app.core.exceptions import ForbiddenError
from app.schemas.account import MeRead, ProfileUpdate
from app.schemas.user import UserRead, UserUpdate
from app.services.account import AccountService, present_account
from app.services.user import UserService


router = APIRouter(prefix="/users", tags=["users"])

_LOCKED_FIELDS = {"role", "organization_id", "permissions", "status", "email"}


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)


@router.get("/me", response_model=MeRead)
async def read_me(
    identity: ClerkIdentity = Depends(require_clerk_identity),
    account: AccountService = Depends(get_account_service),
) -> MeRead:
    user = await account.sync_identity(identity)
    return present_account(user)


@router.patch("/me", response_model=MeRead)
async def update_me(
    payload: ProfileUpdate,
    identity: ClerkIdentity = Depends(require_clerk_identity),
    account: AccountService = Depends(get_account_service),
) -> MeRead:
    user = await account.sync_identity(identity)
    updated = await account.update_profile(user, payload)
    return present_account(updated)


@router.get("", response_model=list[UserRead])
async def list_users(
    identity: ClerkIdentity = Depends(require_clerk_identity),
) -> list[UserRead]:
    del identity
    raise ForbiddenError("The user directory is not available.")


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    identity: ClerkIdentity = Depends(require_clerk_identity),
) -> UserRead:
    del identity
    raise ForbiddenError("Accounts are created when you sign in.")


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    identity: ClerkIdentity = Depends(require_clerk_identity),
    account: AccountService = Depends(get_account_service),
    service: UserService = Depends(get_user_service),
) -> UserRead:
    user = await account.sync_identity(identity)
    if user.id != user_id:
        raise ForbiddenError("You can only access your own profile.")
    return await service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    payload: UserUpdate,
    identity: ClerkIdentity = Depends(require_clerk_identity),
    account: AccountService = Depends(get_account_service),
    service: UserService = Depends(get_user_service),
) -> UserRead:
    user = await account.sync_identity(identity)
    if user.id != user_id:
        raise ForbiddenError("You can only update your own profile.")
    if _LOCKED_FIELDS & payload.model_fields_set:
        raise ForbiddenError("Those account fields cannot be changed.")
    return await service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    identity: ClerkIdentity = Depends(require_clerk_identity),
) -> Response:
    del user_id, identity
    raise ForbiddenError("Account deletion is not available.")
