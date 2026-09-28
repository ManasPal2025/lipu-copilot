"""Account service dependency."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_session
from app.services.account import AccountService


def get_account_service(session: AsyncSession = Depends(get_session)) -> AccountService:
    return AccountService(session)
