"""SQLAlchemy model package.

Import concrete ORM models here as they are introduced so Alembic can discover
their metadata through app.models.base.Base.
"""

from app.models.base import Base, BaseModel, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.communication import CommunicationEvent, Conversation, ConversationMessage
from app.models.consultation_request import ConsultationRequest
from app.models.lead import Lead
from app.models.organization import Organization
from app.models.product import Product
from app.models.product_category import ProductCategory
from app.models.product_interest import ProductInterest
from app.models.product_variant import ProductVariant
from app.models.project import Project
from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.models.transform import TransformAsset, TransformRequest, TransformResult
from app.models.user import User
from app.models.user_profile import UserProfile

__all__ = [
    "Base",
    "BaseModel",
    "CommunicationEvent",
    "ConsultationRequest",
    "Conversation",
    "ConversationMessage",
    "Lead",
    "Organization",
    "Product",
    "ProductCategory",
    "ProductInterest",
    "ProductVariant",
    "Project",
    "Quote",
    "QuoteItem",
    "TimestampMixin",
    "TransformAsset",
    "TransformRequest",
    "TransformResult",
    "UUIDPrimaryKeyMixin",
    "User",
    "UserProfile",
]
