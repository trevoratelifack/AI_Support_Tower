from crewai import Crew, Process
from app.crews.resolution.agents import create_resolution_agent
from app.crews.resolution.tasks import create_resolution_task
from app.models.ticket import SupportTicket
from app.schemas.triage import TriageResult
from app.schemas.investigation import InvestigationResult
from app.schemas.policy import PolicyResult


def run_resolution_crew(ticket: SupportTicket, triage_result: TriageResult, investigation_result: InvestigationResult, policy_result: PolicyResult):
    agent = create_resolution_agent()
    task = create_resolution_task(agent, ticket, triage_result, investigation_result, policy_result)
    result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=True).kickoff()
    return result.pydantic or result.raw
