from crewai import Agent
from app.config import settings
from app.crews.policy.tools import search_policy

def create_policy_agent() -> Agent:
    return Agent(
        role='Policy Agent',
        goal='Accurately determine the applicable policy for a given situation and provide relevant information.',
        backstory="""You are an expert in company policies and procedures. You have years of experience
        understanding and applying policies to various situations. You are able to quickly analyze a situation
        and accurately determine the applicable policy, providing clear and concise information to support decision-making.
        """,
        verbose=True,
        allow_delegation=False,
        llm=settings.model_name,
        tools=[
            search_policy,
        ]
    )
    w
