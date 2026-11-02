from crewai import Crew,Process
from app.crews.investigation.agents import create_investigator_agent
from app.crews.investigation.task import create_investigation_task
from app.models.ticket import SupportTicket
from app.schemas.triage import TriageResult


def run_investigation_crew(
    ticket:SupportTicket,
    triage_result:TriageResult,
):
    """Run the investigation crew"""
    agent = create_investigator_agent()
    task = create_investigation_task(agent,ticket,triage_result)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    result = crew.kickoff()
    return result.pydantic or result.raw
