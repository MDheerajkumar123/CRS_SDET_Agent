from crewai import Agent

from app.llm.crewai_llm import CrewAILLMFactory


class RequirementValidationAgent:
    def __init__(self):
        self.llm = CrewAILLMFactory.create(
            provider_name="openrouter",
            temperature=0.0,
        )

        self.agent = Agent(
            role="Senior SDET Requirement Validation Reviewer",
            goal=(
                "Review requirement analysis for completeness, "
                "accuracy, traceability, testability, and unsupported "
                "inferences without inventing or silently modifying "
                "requirements."
            ),
            backstory=(
                "You are an independent senior SDET reviewer with "
                "expertise in requirements engineering, STLC, "
                "traceability, testability, business rules, and "
                "quality assurance. You critically review requirement "
                "analysis produced by another agent."
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_iter=5,
        )

    def get_agent(self) -> Agent:
        return self.agent
