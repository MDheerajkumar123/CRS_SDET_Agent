import json

from app.llm.manager import LLMManager
from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.models.review_result import TestCaseReviewResult
from app.test_case.validation.prompts.test_case_validator import (
    build_test_case_validator_prompt,
)


class TestCaseValidatorService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def validate(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
        scenario_context: str,
        test_design_context: str,
        test_case_analysis: TestCaseAnalysis,
    ) -> TestCaseReviewResult:

        if not isinstance(test_case_analysis, TestCaseAnalysis):
            raise TypeError(
                "test_case_analysis must be a TestCaseAnalysis instance"
            )

        test_case_context = json.dumps(
            test_case_analysis.model_dump(),
            indent=2,
        )

        prompt = build_test_case_validator_prompt(
            document_name=document_name,
            requirement_context=requirement_context,
            risk_strategy_context=risk_strategy_context,
            scenario_context=scenario_context,
            test_design_context=test_design_context,
            test_case_context=test_case_context,
        )

        response = self.llm_manager.generate(
            task_name="test_case_validator",
            prompt=prompt,
        )

        return self._parse_response(response.content)

    @staticmethod
    def _parse_response(content: str) -> TestCaseReviewResult:
        cleaned = content.strip()

        if cleaned.startswith("```"):
            lines = cleaned.splitlines()

            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned = "\n".join(lines).strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Test Case Validator LLM response is not valid JSON"
            ) from exc

        return TestCaseReviewResult.model_validate(data)
