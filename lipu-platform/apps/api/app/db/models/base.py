"""Placeholder database models

This module contains placeholder ORM models for Sprint 0.
Models will be fully defined in subsequent sprints.
"""

from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid


class BaseModel:
    """Base model with common fields"""

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
