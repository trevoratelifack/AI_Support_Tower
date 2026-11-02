from pydantic import BaseModel, Field


class PolicyResult(BaseModel):
    policy_found: bool
    policy_id: str | None = None
    policy_title: str | None = None
    eligible_for_refund: bool = False
    automatic_action_allowed: bool = False
    requires_human_approval: bool = False
    refund_limit: float | None = None
    evidence: list[str] = Field(default_factory=list)
    policy_summary: str | None = None

    @property
    def automatic_refund(self) -> bool:
        return self.automatic_action_allowed

    @property
    def requires_human_review(self) -> bool:
        return self.requires_human_approval
