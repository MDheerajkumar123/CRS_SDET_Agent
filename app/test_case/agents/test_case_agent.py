from crewai import Agent

from app.llm.crewai_llm import CrewAILLMFactory


class TestCaseAgent:
    def __init__(self):
        self.agent = Agent(
            role="Senior SDET Test Case Engineer",
            goal=(
                "Generate detailed, executable manual test cases from "
                "validated requirements, risk strategy, test scenarios, "
                "and test designs while maintaining strict traceability "
                "and source fidelity."
            ),
            backstory=(
                "You are a Senior SDET Engineer with strong expertise in "
                "software testing, STLC, risk-based testing, test design "
                "techniques, requirements traceability, negative testing, "
                "boundary testing, integration testing, and test case "
                "design. You create precise and independently executable "
                "manual test cases without inventing unsupported system "
                "behavior or implementation details."
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
