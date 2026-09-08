import json

from app.test_case.models.test_case import (
    TestCaseAnalysis,
)
from app.test_case.models.review_result import (
    TestCaseReviewStatus,
    TestCaseReviewResult,
)
from app.test_case.validation.services.test_case_validator_service import (
    TestCaseValidatorService,
)


class FakeLLMManager:
    def generate(self, task_name, prompt):
        assert task_name == "test_case_validator"

        response = {
            "status": "PASS",
            "score": 95,
            "issues": [],
            "required_changes": [],
        }

        class FakeResponse:
            content = json.dumps(response)

        return FakeResponse()


def test_test_case_validator_service():
    test_case_analysis = TestCaseAnalysis(
        document_name="Sample CRS",
        test_case_summary="Sample test cases",
        test_cases=[],
        overall_test_case_confidence=0.9,
    )

    service = TestCaseValidatorService(
        llm_manager=FakeLLMManager()
    )

    result = service.validate(
        document_name="Sample CRS",
        requirement_context="Requirement context",
        risk_strategy_context="Risk strategy context",
        scenario_context="Scenario context",
        test_design_context="Test design context",
        test_case_analysis=test_case_analysis,
    )

    assert isinstance(result, TestCaseReviewResult)
    assert result.status == TestCaseReviewStatus.PASS
    assert result.score == 95

    print("Test Case Validator Service PASS")
