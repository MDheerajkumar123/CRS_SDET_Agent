from crewai import Agent

from app.llm.crewai_llm import CrewAILLMFactory


class TestScenarioAgent:
    def __init__(self):
        self.agent = Agent(
            role="Senior Test Scenario Design Engineer",
            goal=(
                "Generate comprehensive, traceable test scenarios from validated "
                "requirements and risk-based test strategy without inventing "
                "unsupported behavior."
            ),
            backstory=(
                "You are a senior SDET with strong expertise in requirements "
                "analysis, risk-based testing, functional testing, negative testing, "
                "boundary testing, integration testing, usability testing, security "
                "testing, performance testing, compatibility testing, and regression "
                "testing. Every scenario must be traceable to a requirement."
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
