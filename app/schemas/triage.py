from enum import Enum
from pydantic import BaseModel, Field


class TicketCategory(str, Enum):
    TECHNICAL = "technical"
    ACCOUNTS = "accounts"
    BILLING = "billing"
    OTHER = "other"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TicketRisk(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"



class TriageResult(BaseModel):
    """
    Schema for the triage output
    """
    category: TicketCategory 
    priority: TicketPriority
    risk_level: TicketRisk
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="Confidence score of the triage decision (0-1)"
    )
    reasoning: str = Field(
        ...,
        description="Reasoning for the triage decision"
    )