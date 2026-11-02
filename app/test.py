from app.models.ticket import SupportTicket
from app.schemas.triage import TriageResult
from app.crews.investigation.crew import run_investigation_crew


def test_customer_investigation():
    customer_id = "CUST-001"
    ticket_id = "TKT-001"
    ticket = SupportTicket(
        ticket_id=ticket_id,
        customer_id=customer_id,
        subject="Login issue",
        description="I am not able to login to my account"
    )
    triage_result = TriageResult(
        category="technical",
        priority="medium",
        risk_level="low",
        confidence=0.9,
        reasoning="The customer is experiencing a technical issue"
    )
    result = run_investigation_crew(ticket, triage_result)
  

    print("\n\n=== TICKET INVESTIGATION RESULT ===")
    print(result.model_dump_json(indent=2))

    assert result.customer_verified == True
    assert result.customer_name == "John Doe"
    assert result.subscription_status == "active"
    assert result.subscription_plan == "premium"
    assert result.payment_issue_detected == True
    assert result.duplicate_payment == True
    assert result.duplicate_amount == 49.99
    assert result.open_tickets_count == 0
   

if __name__ == "__main__":
    test_customer_investigation()