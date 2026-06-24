"""Base service primitives."""

from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    """Common parent for application services.

    Services orchestrate repositories, external clients, and domain policies.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

