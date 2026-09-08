from crewai import Task

from app.test_case.agents.test_case_agent import TestCaseAgent
from app.test_case.models.test_case import TestCaseAnalysis


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
        description = f"""
        Generate detailed manual test cases for the document:
        {self.document_name}

        Requirement Context:
        {self.requirement_context}

        Risk & Test Strategy Context:
        {self.risk_strategy_context}

        Test Scenario Context:
        {self.scenario_context}

        Test Design Context:
        {self.test_design_context}

        Follow the Test Case generation rules strictly.

        Maintain complete traceability:
        Requirement → Scenario → Test Design → Test Case.

        Do not invent unsupported requirements, business rules,
        implementation details, or exact test data.

        Generate executable manual test steps and corresponding
        expected results.

        Return the result as TestCaseAnalysis.
        """

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
