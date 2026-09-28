"""Closed vocabularies for the Ecotech platform foundation."""

from enum import Enum


class UserRole(str, Enum):
    GUEST = "guest"
    CUSTOMER = "customer"
    ADMIN = "admin"
    SALES = "sales"


class LeadSource(str, Enum):
    WEBSITE = "WEBSITE"
    CONSULTATION = "CONSULTATION"
    PRODUCT = "PRODUCT"
    TRANSFORM = "TRANSFORM"
    CHATBOT = "CHATBOT"
    WHATSAPP = "WHATSAPP"
    PHONE = "PHONE"


class LeadStatus(str, Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    PROPOSAL = "PROPOSAL"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    LOST = "LOST"
    CLOSED = "CLOSED"


class LeadPriority(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class ProjectType(str, Enum):
    RESIDENTIAL = "RESIDENTIAL"
    RENOVATION = "RENOVATION"
    COMMERCIAL = "COMMERCIAL"
    HOSPITALITY = "HOSPITALITY"
    ARCHITECTURAL = "ARCHITECTURAL"
    ARCHITECT = "ARCHITECT"
    OTHER = "OTHER"


class ProjectStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ProductArea(str, Enum):
    WINDOWS = "WINDOWS"
    DOORS = "DOORS"
    ARCHITECTURAL_SYSTEMS = "ARCHITECTURAL_SYSTEMS"
    CUSTOM_OPENINGS = "CUSTOM_OPENINGS"


class TransformTarget(str, Enum):
    WINDOWS = "WINDOWS"
    DOORS = "DOORS"
    BALCONY = "BALCONY"
    TERRACE = "TERRACE"
    OUTDOOR = "OUTDOOR"


class TransformVariant(str, Enum):
    SLIDING = "SLIDING"
    CASEMENT = "CASEMENT"
    LARGE_OPENING = "LARGE_OPENING"
    BIFOLD = "BIFOLD"
    FRENCH = "FRENCH"


class TransformStatus(str, Enum):
    UPLOADED = "UPLOADED"
    CONFIGURED = "CONFIGURED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TransformAssetType(str, Enum):
    SOURCE = "SOURCE"
    RESULT = "RESULT"
    REFERENCE = "REFERENCE"


class ContactMethod(str, Enum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    WHATSAPP = "WHATSAPP"


class ConversationChannel(str, Enum):
    WEB = "WEB"
    EMAIL = "EMAIL"
    WHATSAPP = "WHATSAPP"


class ConversationStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class MessageSender(str, Enum):
    GUEST = "GUEST"
    USER = "USER"
    STAFF = "STAFF"
    SYSTEM = "SYSTEM"


class CommunicationEventType(str, Enum):
    CONSULTATION_RECEIVED = "CONSULTATION_RECEIVED"
    EMAIL_SENT = "EMAIL_SENT"
    WHATSAPP_SENT = "WHATSAPP_SENT"
    CHAT_STARTED = "CHAT_STARTED"
    CHAT_ESCALATED = "CHAT_ESCALATED"
    LEAD_CREATED = "LEAD_CREATED"
    LEAD_UPDATED = "LEAD_UPDATED"


def enum_values(enum_cls: type[Enum]) -> tuple[str, ...]:
    return tuple(member.value for member in enum_cls)


def sql_in(column: str, enum_cls: type[Enum]) -> str:
    values = ", ".join(f"'{value}'" for value in enum_values(enum_cls))
    return f"{column} IN ({values})"
