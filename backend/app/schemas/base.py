"""Shared Pydantic schema primitives."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class APIModel(BaseModel):
    """Base Pydantic model with ORM attribute support."""

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class EntityRead(APIModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

