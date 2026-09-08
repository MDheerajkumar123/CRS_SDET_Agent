from crewai import Agent

from app.llm.crewai_llm import CrewAILLMFactory


class ScenarioValidationAgent:
    def __init__(self):
        self.agent = Agent(
            role="Senior Test Scenario Validation Engineer",
            goal=(
                "Independently review generated test scenarios against "
                "validated requirements and the risk-based test strategy, "
                "identify gaps or unsupported assumptions, and determine "
                "whether the scenarios are ready for test design."
            ),
            backstory=(
                "You are a senior SDET and QA reviewer with strong expertise "
                "in requirements traceability, risk-based testing, positive "
                "testing, negative testing, boundary testing, error handling, "
                "integration testing, security testing, performance testing, "
                "usability testing, compatibility testing, and regression "
                "testing. You are independent from the scenario-generation "
                "agent and must not approve scenarios that contain "
                "unsupported requirements or hallucinated behavior."
            ),
            llm=CrewAILLMFactory.create(
                provider_name="openrouter",
                temperature=0.0,
            ),
            verbose=True,
            allow_delegation=False,
            max_iter=5,
        )

    def get_agent(self):
        return self.agent
