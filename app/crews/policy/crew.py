from crewai import Crew, Process

from app.models.ticket import SupportTicket
from app.schemas.triage import TriageResult
from app.schemas.investigation import InvestigationResult

from app.crews.policy.agents import create_policy_agent
from app.crews.policy.tasks import create_policy_task

def run_policy_crew(
    ticket: SupportTicket,
    triage_result: TriageResult,
    investigation_result: InvestigationResult
):
    """Run the policy crew"""
    agent = create_policy_agent()
    task = create_policy_task(agent, ticket, triage_result, investigation_result)
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    result = crew.kickoff()
    return result.pydantic or result.raw