from crewai import Agent
from app.config import settings


def create_resolution_agent() -> Agent:
    return Agent(
        role="Resolution Recommendation Agent",
        goal="Recommend a supported customer service action using investigation facts and policy evidence.",
        backstory="You are a cautious operations specialist. Recommend actions only; never execute refunds, cancellations, account changes, or messages. Escalate when facts or policy do not support a safe recommendation.",
        verbose=True,
        allow_delegation=False,
        llm=settings.model_name,
    )
