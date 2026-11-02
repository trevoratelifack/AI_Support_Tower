from crewai import Task
from app.models.ticket import SupportTicket
from app.schemas.triage import TriageResult
from app.schemas.investigation import InvestigationResult
from app.schemas.policy import PolicyResult
from app.schemas.resolution import ResolutionResult


def create_resolution_task(agent, ticket: SupportTicket, triage: TriageResult, investigation: InvestigationResult, policy: PolicyResult) -> Task:
    return Task(
        description=f"""Recommend one action for this support case. Do not execute the action.
Ticket: {ticket.model_dump_json()}
Triage: {triage.model_dump_json()}
Investigation: {investigation.model_dump_json()}
Policy: {policy.model_dump_json()}

Only recommend a refund when duplicate payment is confirmed and policy allows it. Set approval_required
when policy requires approval or evidence is incomplete. Do not invent facts. If unresolved, escalate or
request more information. The amount is the single duplicate charge, not the total of both charges.""",
        expected_output="A ResolutionResult with recommended_action, action_reason, amount, confidence, approval_required, supporting_evidence, and customer_response_summary.",
        output_pydantic=ResolutionResult,
        agent=agent,
    )
