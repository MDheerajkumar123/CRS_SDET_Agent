
from crewai import Agent

from app.llm.crewai_llm import CrewAILLMFactory


class RTMAgent:
    def __init__(self):
        self.llm = CrewAILLMFactory.create(
            provider_name="openrouter",
            temperature=0.0,
        )

        self.agent = Agent(
            role="Senior SDET RTM and Coverage Analyst",
            goal=(
                "Create an accurate, evidence-based Requirement "
                "Traceability Matrix by tracing requirements through "
                "test scenarios, test designs, and test cases."
            ),
            backstory=(
                "You are a senior SDET and QA traceability specialist "
                "with strong expertise in requirements analysis, "
                "test coverage, risk-based testing, and RTM creation. "
                "You never invent identifiers or unsupported "
                "relationships. Every traceability decision must be "
                "supported by the supplied project artifacts."
            ),
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
            max_iter=5,
        )

    def get_agent(self) -> Agent:
        return self.agent
