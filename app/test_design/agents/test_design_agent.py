from crewai import Agent

from app.llm.crewai_llm import CrewAILLMFactory


class TestDesignAgent:
    def __init__(self):
        self.agent = Agent(
            role="Senior SDET Test Design Engineer",
            goal=(
                "Convert validated requirements, risk strategy, and test "
                "scenarios into traceable and risk-based test designs."
            ),
            backstory=(
                "You are a senior SDET with strong expertise in software "
                "testing, test design techniques, risk-based testing, "
                "requirements traceability, and STLC practices. "
                "You design tests strictly from approved source information "
                "and never invent requirements or implementation details."
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
