from crewai import Agent
from app.config import settings
from app.crews.investigation.tools import get_customer, get_subscription, get_payment_history, get_ticket_history



def create_investigator_agent()->Agent:
    return Agent(
        role='Ticket Investigation Agent',
        goal='Gather verifiable customer, subscription, payment, and ticket history facts relevant to the ticket.',
        backstory="""You are a careful customer support investigator. Use the available records as evidence.
        You never make business decisions, alter accounts, issue refunds, cancel subscriptions, or contact customers.
        Never infer customer facts that are absent from the records.
        """,
        verbose=True,
        allow_delegation=False,
        llm=settings.model_name,
        tools=[
            get_customer,
            get_subscription,
            get_payment_history,
            get_ticket_history,
        ]
    )
