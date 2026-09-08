from crewai import Agent

from app.llm.crewai_llm import CrewAILLMFactory


class TestCaseValidationAgent:
    def __init__(self):
        self.agent = Agent(
            role="Senior SDET Test Case Validation Reviewer",
            goal=(
                "Independently validate generated test cases against the "
                "requirements, risk strategy, scenarios, and test designs. "
                "Identify traceability defects, hallucinations, unsupported "
                "assumptions, coverage gaps, duplicates, and testability issues."
            ),
            backstory=(
                "You are a senior SDET and QA reviewer with strong expertise "
                "in STLC, risk-based testing, test design techniques, "
                "requirements traceability, negative and boundary testing, "
                "integration testing, and test case quality. "
                "You are an independent reviewer. You must not invent "
                "requirements or implementation details. You validate the "
                "generated test cases strictly against the supplied source "
                "information."
            ),
            llm=CrewAILLMFactory.create(
                provider_name="openrouter",
                temperature=0.0,
            ),
            allow_delegation=False,
            max_iter=5,
            verbose=True,
        )

    def get_agent(self) -> Agent:
        return self.agent
