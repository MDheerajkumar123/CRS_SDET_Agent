from crewai import Crew, Process

from app.test_case.validation.agents.test_case_validation_agent import (
    TestCaseValidationAgent,
)
from app.test_case.validation.tasks.test_case_validation_task import (
    TestCaseValidationTask,
)


class TestCaseValidationCrew:
    def __init__(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
        scenario_context: str,
        test_design_context: str,
        test_case_context: str,
    ):
        self.document_name = document_name
        self.requirement_context = requirement_context
        self.risk_strategy_context = risk_strategy_context
        self.scenario_context = scenario_context
        self.test_design_context = test_design_context
        self.test_case_context = test_case_context

    def build(self) -> Crew:
        agent = TestCaseValidationAgent().get_agent()

        task = TestCaseValidationTask(
            document_name=self.document_name,
            requirement_context=self.requirement_context,
            risk_strategy_context=self.risk_strategy_context,
            scenario_context=self.scenario_context,
            test_design_context=self.test_design_context,
            test_case_context=self.test_case_context,
        ).create_task()

        return Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True,
        )
