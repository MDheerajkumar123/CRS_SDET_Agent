from crewai import Task

from app.strategy.agents.risk_strategy_agent import RiskStrategyAgent
from app.strategy.models.test_strategy import TestStrategy
from app.strategy.prompts.test_strategy import build_test_strategy_prompt


class RiskStrategyTask:
    def __init__(
        self,
        document_name: str,
        requirement_context: str,
    ):
        self.document_name = document_name
        self.requirement_context = requirement_context

    def create_task(self) -> Task:
        agent = RiskStrategyAgent().get_agent()

        prompt = build_test_strategy_prompt(
            document_name=self.document_name,
            requirement_context=self.requirement_context,
        )

        return Task(
            description=prompt,
            expected_output=(
                "A valid JSON object conforming exactly to the "
                "TestStrategy schema."
            ),
            agent=agent,
            output_pydantic=TestStrategy,
        )
