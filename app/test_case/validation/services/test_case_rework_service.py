import json

from app.llm.manager import LLMManager
from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.validation.models.rework_request import (
    TestCaseReworkRequest,
)
from app.test_case.validation.prompts.rework_prompt import (
    build_test_case_rework_prompt,
)


class TestCaseReworkService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def rework(
        self,
        request: TestCaseReworkRequest,
    ) -> TestCaseAnalysis:

        if not isinstance(request, TestCaseReworkRequest):
            raise TypeError(
                "request must be a TestCaseReworkRequest instance"
            )

        prompt = build_test_case_rework_prompt(
            document_name=request.document_name,
            current_test_cases=request.current_test_cases,
            issues=request.issues,
            required_changes=request.required_changes,
            retry_count=request.retry_count,
        )

        response = self.llm_manager.generate(
            task_name="test_case",
            prompt=prompt,
        )

        return self._parse_response(response.content)

    @staticmethod
    def _parse_response(content: str) -> TestCaseAnalysis:
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
                "Test Case Rework LLM response is not valid JSON"
            ) from exc

        return TestCaseAnalysis.model_validate(data)
