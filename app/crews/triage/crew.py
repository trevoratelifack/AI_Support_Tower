from crewai import Crew, Process
from app.crews.triage.agents import create_triage_agent
from app.crews.triage.tasks import  create_triage_task
from app.models.ticket import SupportTicket


def run_triage_crew(ticket: SupportTicket):

    agent = create_triage_agent()
    task=create_triage_task(agent,ticket)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    result = crew.kickoff()
    
    return result.pydantic or result.raw


if __name__ == "__main__":
    ticket = SupportTicket(
        ticket_id="TKT-001",
        customer_id="CUST-001",
        subject="Login issue",
        description="I am not able to login to my account"
    )
    result = run_triage_crew(ticket)
    print(result)