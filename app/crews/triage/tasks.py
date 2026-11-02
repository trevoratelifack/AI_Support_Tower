from crewai import Task

from app.models.ticket import SupportTicket
from app.schemas.triage import TriageResult

def create_triage_task(
    agent,
    ticket: SupportTicket,
   
) -> Task:
    return Task(
        description=f""" Analyze the following customer support ticket.
        Ticket ID:
        {ticket.ticket_id}
        
        Customer ID:
        {ticket.customer_id}
        
        Subject:
        {ticket.subject}
        
        Description:
        {ticket.description}

        Determine:
        1. The customer's primary intent.
        2. The best category for this ticket (technical, accounts, billing, other)
        3. The priority of the ticket (low, medium, high, urgent)
        4. The risk level of the ticket (low, medium, high)
        5. The confidence score of the triage decision (0-1)
        6. The reasoning for the triage decision

        DO NOT invent information that is not contained in the ticket. If there is not enough information to make a decision, ask for clarification
        """,
        expected_output=("A structured TriageResults containing intent, category, priority, risk_level, confidence and reasoning for the triage decision"),
        output_pydantic=TriageResult,
        agent=agent

    )