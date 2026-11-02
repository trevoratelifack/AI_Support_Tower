from enum import Enum
from pydantic import BaseModel, Field


class RecommendedAction(str, Enum):
    REFUND_PAYMENT = "refund_payment"
    CANCEL_SUBSCRIPTION = "cancel_subscription"
    SEND_INVOICE = "send_invoice"
    PROVIDE_PAYMENT_INSTRUCTIONS = "provide_payment_instructions"
    REQUEST_MORE_INFORMATION = "request_more_information"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    NO_ACTION = "no_action"


class ResolutionResult(BaseModel):
    recommended_action: RecommendedAction
    action_reason: str
    amount: float | None = None
    confidence: float = Field(ge=0, le=1)
    approval_required: bool = False
    supporting_evidence: list[str] = Field(default_factory=list)
    customer_response_summary: str
