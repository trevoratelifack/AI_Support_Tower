from crewai import Task

from app.models.ticket import SupportTicket
from app.schemas.investigation import InvestigationResult
from app.schemas.policy import PolicyResult
from app.schemas.triage import TriageResult


def create_policy_task(
    agent,
    ticket: SupportTicket,
    triage_result: TriageResult,
    investigation_result: InvestigationResult,
) -> Task:
    return Task(
        description=f"""Determine the policy outcome for this support ticket.

        Ticket ID: {ticket.ticket_id}
        Customer ID: {ticket.customer_id}
        Subject: {ticket.subject}
        Description: {ticket.description}

        Triage result:
        Category: {triage_result.category}
        Priority: {triage_result.priority}
        Risk level: {triage_result.risk_level}
        Reasoning: {triage_result.reasoning}

        Investigation result:
        Customer verified: {investigation_result.customer_verified}
        Customer name: {investigation_result.customer_name}
        Subscription status: {investigation_result.subscription_status}
        Payment issue detected: {investigation_result.payment_issue_detected}
        Duplicate payment: {investigation_result.duplicate_payment}
        Duplicate amount: {investigation_result.duplicate_amount}
        Evidence: {investigation_result.evidence}
        Investigation summary: {investigation_result.investigation_summary}

        Apply the relevant policy to the available facts. Do not invent facts,
        issue a refund, or make changes to the customer's account. If policy
        eligibility cannot be determined from the evidence, say so in the
        summary and require human review.
        """,
        expected_output=(
            "A structured PolicyResult with policy_found, eligible_for_refund, "
        "automatic_action_allowed, requires_human_approval, refund_limit, policy_id, policy_title, evidence, "
            "and policy_summary."
        ),
        output_pydantic=PolicyResult,
        agent=agent,
    )
