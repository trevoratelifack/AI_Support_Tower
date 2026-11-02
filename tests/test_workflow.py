from app.crews.investigation.tools import customer_record, payment_records, ticket_records
from app.crews.policy.tools import find_policies
from app.flows import support_flow as flow_module
from app.models.ticket import SupportTicket
from app.schemas.investigation import InvestigationResult
from app.schemas.policy import PolicyResult
from app.schemas.resolution import RecommendedAction, ResolutionResult
from app.schemas.triage import TriageResult, TicketCategory, TicketPriority, TicketRisk


def sample_results():
    triage = TriageResult(category=TicketCategory.BILLING, priority=TicketPriority.HIGH, risk_level=TicketRisk.MEDIUM, confidence=.96, reasoning="Duplicate charge reported")
    investigation = InvestigationResult(customer_verified=True, customer_name="Jordan Lee", subscription_status="active", subscription_plan="Pro", payment_issue_detected=True, duplicate_payment=True, duplicate_amount=49, evidence=["Two successful payments for 2026-10"], investigation_summary="Duplicate confirmed")
    policy = PolicyResult(policy_found=True, policy_id="POL-001", policy_title="Duplicate Payment Refund Policy", eligible_for_refund=True, automatic_action_allowed=True, requires_human_approval=False, refund_limit=100, evidence=["Limit is 100 EUR"], policy_summary="Eligible")
    return triage, investigation, policy


def test_investigation_synthetic_sources_are_deterministic():
    assert customer_record("CUS-001")["name"] == "Jordan Lee"
    charges = [payment for payment in payment_records("CUS-001") if payment["status"] == "succeeded"]
    assert len(charges) == 2 and charges[0]["amount"] == charges[1]["amount"] == 49
    assert ticket_records("CUS-999") == []
    assert not customer_record("CUS-999")


def test_policy_search_covers_duplicate_and_invoice():
    assert find_policies("duplicate payment")[0]["id"] == "POL-001"
    assert find_policies("invoice request")[0]["id"] == "POL-004"
    assert PolicyResult(policy_found=True, refund_limit=100).refund_limit == 100


def test_resolution_contract_supports_recommendation_and_escalation():
    resolution = ResolutionResult(recommended_action=RecommendedAction.REFUND_PAYMENT, action_reason="Confirmed duplicate within limit", amount=49, confidence=.94, approval_required=False, supporting_evidence=["POL-001"], customer_response_summary="We found a duplicate charge.")
    assert resolution.recommended_action == RecommendedAction.REFUND_PAYMENT
    assert resolution.amount == 49 and not resolution.approval_required
    missing = ResolutionResult(recommended_action=RecommendedAction.ESCALATE_TO_HUMAN, action_reason="Customer could not be verified", confidence=.5, approval_required=True, customer_response_summary="We need to review your account.")
    assert missing.approval_required


def test_full_flow_passes_structured_results_between_stages(monkeypatch):
    triage, investigation, policy = sample_results()
    resolution = ResolutionResult(recommended_action=RecommendedAction.REFUND_PAYMENT, action_reason="Confirmed and within limit", amount=49, confidence=.94, supporting_evidence=["Two successful charges", "POL-001"], customer_response_summary="Duplicate charge identified.")
    monkeypatch.setattr(flow_module, "run_triage_crew", lambda ticket: triage)
    monkeypatch.setattr(flow_module, "run_investigation_crew", lambda ticket, triage_result: investigation)
    monkeypatch.setattr(flow_module, "run_policy_crew", lambda ticket, triage_result, investigation_result: policy)
    monkeypatch.setattr(flow_module, "run_resolution_crew", lambda ticket, triage_result, investigation_result, policy_result: resolution)

    flow = flow_module.SupportFlow()
    flow.kickoff(inputs=SupportTicket(ticket_id="TCK-1001", customer_id="CUS-001", subject="Duplicate payment", description="Charged twice").model_dump())

    assert flow.state["triage_result"] is triage
    assert flow.state["investigation_result"] is investigation
    assert flow.state["policy_result"] is policy
    assert flow.state["resolution_result"].recommended_action == RecommendedAction.REFUND_PAYMENT

