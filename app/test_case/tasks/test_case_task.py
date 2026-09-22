from crewai import Task

from app.test_case.agents.test_case_agent import TestCaseAgent
from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.prompts.test_case import build_test_case_prompt


class TestCaseTask:
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

        self.agent = TestCaseAgent().get_agent()

    def create_task(self) -> Task:
        description = build_test_case_prompt(
            document_name=self.document_name,
            requirement_context=self.requirement_context,
            risk_strategy_context=self.risk_strategy_context,
            scenario_context=self.scenario_context,
            test_design_context=self.test_design_context,
        )

        expected_output = """
        A validated TestCaseAnalysis containing:
        - document_name
        - test_case_summary
        - test_cases
        - overall_test_case_confidence

        Every test case must contain valid:
        - test_case_id
        - design_id
        - scenario_id
        - requirement_id
        - title
        - objective
        - test_type
        - priority
        - preconditions
        - test_data
        - steps
        - expected_results
        - source_design
        """

        return Task(
            description=description,
            expected_output=expected_output,
            agent=self.agent,
            output_pydantic=TestCaseAnalysis,
        )
