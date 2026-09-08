from crewai import Crew, Process

from app.test_design.agents.test_design_agent import TestDesignAgent
from app.test_design.tasks.test_design_task import TestDesignTask


class TestDesignCrew:
    def __init__(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
        scenario_context: str,
    ):
        self.document_name = document_name
        self.requirement_context = requirement_context
        self.risk_strategy_context = risk_strategy_context
        self.scenario_context = scenario_context

    def build(self) -> Crew:
        agent = TestDesignAgent().get_agent()

        task = TestDesignTask(
            document_name=self.document_name,
            requirement_context=self.requirement_context,
            risk_strategy_context=self.risk_strategy_context,
            scenario_context=self.scenario_context,
        ).create_task()

        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )
