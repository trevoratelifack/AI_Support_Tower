"""Synthetic support data access; replace these functions with provider adapters later."""
from crewai.tools import tool

CUSTOMERS = {
    "CUS-001": {"id": "CUS-001", "name": "Jordan Lee", "email": "jordan@example.test"},
    "CUS-002": {"id": "CUS-002", "name": "Morgan Chen", "email": "morgan@example.test"},
}
SUBSCRIPTIONS = {
    "CUS-001": {"plan": "Pro", "status": "active", "subscription_id": "SUB-001"},
    "CUS-002": {"plan": "Basic", "status": "past_due", "subscription_id": "SUB-002"},
}
PAYMENTS = {
    "CUS-001": [
        {"id": "PAY-101", "period": "2026-10", "amount": 49.0, "currency": "EUR", "status": "succeeded"},
        {"id": "PAY-102", "period": "2026-10", "amount": 49.0, "currency": "EUR", "status": "succeeded"},
    ],
    "CUS-002": [{"id": "PAY-201", "period": "2026-10", "amount": 29.0, "currency": "EUR", "status": "failed"}],
}
TICKET_HISTORY = {
    "CUS-001": [],
    "CUS-002": [{"id": "TCK-0999", "subject": "Payment failed", "status": "open"}],
}


def customer_record(customer_id: str) -> dict:
    return CUSTOMERS.get(customer_id, {})


def subscription_record(customer_id: str) -> dict:
    return SUBSCRIPTIONS.get(customer_id, {})


def payment_records(customer_id: str) -> list[dict]:
    return PAYMENTS.get(customer_id, [])


def ticket_records(customer_id: str) -> list[dict]:
    return TICKET_HISTORY.get(customer_id, [])


@tool("get_customer")
def get_customer(customer_id: str) -> dict:
    """Retrieve a synthetic customer record by customer ID."""
    record = customer_record(customer_id)
    return {"found": bool(record), "customer": record or None}


@tool("get_subscription")
def get_subscription(customer_id: str) -> dict:
    """Retrieve the customer's subscription status and plan."""
    record = subscription_record(customer_id)
    return {"found": bool(record), "subscription": record or None}


@tool("get_payment_history")
def get_payment_history(customer_id: str) -> dict:
    """Retrieve recent payment records for a customer."""
    return {"payments": payment_records(customer_id)}


@tool("get_ticket_history")
def get_ticket_history(customer_id: str) -> dict:
    """Retrieve previous support tickets for a customer."""
    return {"tickets": ticket_records(customer_id)}


# Backward-compatible tool name for the original investigation implementation.
get_payment = get_payment_history
