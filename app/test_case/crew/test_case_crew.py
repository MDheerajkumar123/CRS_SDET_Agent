from crewai import Crew, Process

from app.test_case.agents.test_case_agent import TestCaseAgent
from app.test_case.tasks.test_case_task import TestCaseTask


class TestCaseCrew:
    def __init__(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
        scenario_context: str,
        test_design_context: str,
    ):
        self.document_name = document_name
        self.requirement_context = requirement_context
        self.risk_strategy_context = risk_strategy_context
        self.scenario_context = scenario_context
        self.test_design_context = test_design_context

    def build(self) -> Crew:
        agent = TestCaseAgent().get_agent()

        task = TestCaseTask(
            document_name=self.document_name,
            requirement_context=self.requirement_context,
            risk_strategy_context=self.risk_strategy_context,
            scenario_context=self.scenario_context,
            test_design_context=self.test_design_context,
        ).create_task()

        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )
