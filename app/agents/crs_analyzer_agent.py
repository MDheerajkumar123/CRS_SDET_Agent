from crewai import Agent

from app.agents.tools.crs_analyzer_tool import (
    CRSAnalyzerTool,
)
from app.llm.crewai_llm import CrewAILLMFactory


class CRSAnalyzerAgent:
    """
    CrewAI wrapper for the CRS Requirement Analysis role.
    """

    def __init__(self):
        self.analyzer_tool = CRSAnalyzerTool()

        self.llm = CrewAILLMFactory.create(
            provider_name="openrouter",
            temperature=0.0,
        )

        self.agent = Agent(
            role="Senior SDET Requirement Analysis Agent",
            goal=(
                "Analyze CRS requirements accurately, preserve "
                "traceability, and identify testable requirements "
                "without hallucinating missing information."
            ),
            backstory=(
                "You are a senior SDET specializing in requirement "
                "analysis, business-rule identification, requirement "
                "traceability, and testability assessment."
            ),
            llm=self.llm,
            tools=[self.analyzer_tool],
            verbose=True,
            allow_delegation=False,
            max_iter=5,
        )

    def get_agent(self) -> Agent:
        return self.agent
