from pydantic import BaseModel, Field


class InvestigationResult(BaseModel):
    customer_verified: bool
    customer_name: str | None = None
    subscription_status: str | None = None
    subscription_plan: str | None = None
    payment_issue_detected: bool = False
    duplicate_payment: bool = False
    duplicate_amount: float | None = None
    relevant_previous_tickets: list[dict] = Field(default_factory=list)
    open_tickets_count: int = 0
    evidence: list[str] = Field(default_factory=list)
    investigation_summary: str
