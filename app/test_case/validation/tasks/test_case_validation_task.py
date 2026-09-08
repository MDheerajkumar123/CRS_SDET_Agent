from crewai import Task

from app.test_case.models.review_result import TestCaseReviewResult
from app.test_case.validation.agents.test_case_validation_agent import (
    TestCaseValidationAgent,
)
from app.test_case.validation.prompts.test_case_validator import (
    build_test_case_validator_prompt,
)


class TestCaseValidationTask:
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

    def create_task(self) -> Task:
        agent = TestCaseValidationAgent().get_agent()

        description = build_test_case_validator_prompt(
            document_name=self.document_name,
            requirement_context=self.requirement_context,
            risk_strategy_context=self.risk_strategy_context,
            scenario_context=self.scenario_context,
            test_design_context=self.test_design_context,
            test_case_context=self.test_case_context,
        )

        return Task(
            description=description,
            expected_output=(
                "A JSON test case review containing status, score, issues, "
                "and required_changes."
            ),
            agent=agent,
            output_pydantic=TestCaseReviewResult,
        )
