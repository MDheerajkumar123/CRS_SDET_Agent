from crewai import Crew, Process

from app.strategy.agents.risk_strategy_agent import RiskStrategyAgent
from app.strategy.tasks.risk_strategy_task import RiskStrategyTask


class RiskStrategyCrew:
    def __init__(
        self,
        document_name: str,
        requirement_context: str,
    ):
        self.document_name = document_name
        self.requirement_context = requirement_context

    def build(self) -> Crew:
        agent = RiskStrategyAgent().get_agent()

        task = RiskStrategyTask(
            document_name=self.document_name,
            requirement_context=self.requirement_context,
        ).create_task()

        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )
