from crewai import Agent
from app.config import settings

def create_triage_agent() -> Agent:
    return Agent(
        role='Ticket Triage Agent',
        goal='Accurately categorize and prioritize support tickets based on their content and context.',
        backstory="""You are an expert in IT support and customer service. You have years of experience 
        categorizing and prioritizing support tickets. You are able to quickly understand the 
        content and context of a support ticket and accurately categorize and prioritize it.
        """,
        verbose=True,
        allow_delegation=False,
        llm=settings.model_name
        
    )