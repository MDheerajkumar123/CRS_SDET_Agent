
from crewai import Agent

from app.llm.crewai_llm import CrewAILLMFactory


class FinalQAReviewerAgent:
    def __init__(self):
        self.agent = Agent(
            role="Senior SDET Final QA Reviewer",
            goal=(
                "Independently review the complete QA package for "
                "requirements completeness, traceability, coverage, "
                "consistency, source fidelity, and final delivery readiness."
            ),
            backstory=(
                "You are a senior SDET and QA lead responsible for the "
                "final quality gate. You review requirements, risk strategy, "
                "scenarios, test designs, test cases, and the RTM as one "
                "integrated QA package. You never invent requirements, IDs, "
                "relationships, implementation details, or execution "
                "capabilities. You approve only evidence-based deliverables."
            ),
            llm=CrewAILLMFactory.create(
                provider_name="openrouter",
                temperature=0.0,
            ),
            allow_delegation=False,
            verbose=True,
            max_iter=5,
        )

    def get_agent(self) -> Agent:
        return self.agent
