
from crewai import Agent

from app.llm.crewai_llm import CrewAILLMFactory


class RTMValidationAgent:
    def __init__(self):
        self.agent = Agent(
            role="Senior SDET RTM Validation Reviewer",
            goal=(
                "Independently review the RTM for completeness, "
                "traceability, coverage accuracy, evidence quality, "
                "and source fidelity without inventing relationships."
            ),
            backstory=(
                "You are a senior SDET and QA traceability reviewer. "
                "You validate requirement-to-scenario-to-test-design-to-test-case "
                "coverage using only the supplied evidence. "
                "You identify missing, partial, incorrect, duplicated, or "
                "unsupported traceability and provide precise rework guidance."
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
