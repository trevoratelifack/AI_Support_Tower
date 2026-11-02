"""Local policy search behind a replaceable retrieval interface."""
from crewai.tools import tool

POLICIES = [
    {"id": "POL-001", "type": "duplicate_payment", "title": "Duplicate Payment Refund Policy", "content": "Two successful payments for the same subscription period may be refunded. Duplicate refunds of 100 EUR or less may be processed automatically. Above 100 EUR requires human approval.", "refund_limit": 100.0},
    {"id": "POL-002", "type": "subscription_cancellation", "title": "Subscription Cancellation Policy", "content": "A customer may request subscription cancellation. Cancellation follows the customer's subscription terms. Refund eligibility is evaluated separately."},
    {"id": "POL-003", "type": "failed_payment", "title": "Failed Payment Policy", "content": "A failed payment may leave an account in a grace period. Explain the payment failure and provide payment instructions; do not claim payment succeeded."},
    {"id": "POL-004", "type": "invoice_request", "title": "Invoice Request Policy", "content": "A verified customer may request an invoice for a completed payment. Confirm the payment and billing details before issuing an invoice."},
]


def find_policies(query: str) -> list[dict]:
    """Search local policies; replace this with an embeddings/BM25 adapter later."""
    terms = set(query.lower().replace("_", " ").split())
    matches = []
    for policy in POLICIES:
        searchable = f"{policy['type']} {policy['title']} {policy['content']}".lower()
        score = sum(term in searchable for term in terms if len(term) > 2)
        if score:
            matches.append({**policy, "score": score})
    return sorted(matches, key=lambda item: item["score"], reverse=True)


@tool("search_policy")
def search_policy(query: str) -> list[dict]:
    """Find relevant policy entries in the approved local policy knowledge base."""
    return find_policies(query)
