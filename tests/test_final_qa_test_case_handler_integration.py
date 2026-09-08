
import json

from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.final_review.models.review_result import (
    FinalQAReviewResult,
    FinalReviewStatus,
)
from app.final_review.services.final_qa_rework_service import (
    FinalQAReworkResult,
)
from app.final_review.services.final_qa_validation_loop import (
    FinalQAValidationLoop,
)
from app.final_review.services.handlers.test_case_rework_handler import (
    TestCaseReworkHandler,
)
from app.test_case.models.test_case import (
    TestCaseAnalysis,
)


class FakeReviewer:
    def __init__(self):
        self.calls = 0

    def review(self, **kwargs):
        self.calls += 1

        if self.calls == 1:
            return FinalQAReviewResult(
                status=FinalReviewStatus.REWORK,
                score=70,
                issues=["Test case coverage gap"],
                required_changes=[
                    "Add missing test case coverage."
                ],
                review_summary="Test case rework required.",
            )

        return FinalQAReviewResult(
            status=FinalReviewStatus.PASS,
            score=95,
            review_summary="Approved after test case rework.",
        )


class FakeFinalQAReworkService:
    def rework(self, request):
        return FinalQAReworkResult(
            document_name=request.document_name,
            rework_targets=[
                {
                    "artifact": "TEST_CASES",
                    "reason": "Test case coverage gap",
                    "actions": [
                        "Add missing test case coverage."
                    ],
                }
            ],
            overall_rework_summary=(
                "Test cases require rework."
            ),
        )


class FakeTestCaseReworkService:
    def __init__(self):
        self.calls = 0

    def rework(self, request):
        self.calls += 1

        return TestCaseAnalysis(
            document_name=request.document_name,
            test_case_summary=(
                "Test cases revised by Test Case workflow."
            ),
            test_cases=[],
            overall_test_case_confidence=0.95,
        )


def test_final_qa_routes_test_case_rework_to_real_handler_adapter():
    reviewer = FakeReviewer()

    final_qa_rework_service = FakeFinalQAReworkService()

    test_case_rework_service = FakeTestCaseReworkService()

    test_case_handler = TestCaseReworkHandler(
        rework_service=test_case_rework_service
    )

    captured = {}

    def rework_handler(
        request,
        rework_result,
        routing_result,
        current_context,
    ):
        captured["routing_result"] = routing_result

        assert routing_result["routes"][0]["artifact"] == (
            "TEST_CASES"
        )

        assert routing_result["routes"][0]["route"] == (
            "test_case_validation"
        )

        updated_context = test_case_handler.handle(
            request=request,
            rework_result=rework_result,
            routing_result=routing_result,
            current_context=current_context,
        )

        captured["updated_context"] = updated_context

        return updated_context

    loop = FinalQAValidationLoop(
        reviewer_service=reviewer,
        rework_service=final_qa_rework_service,
        rework_handler=rework_handler,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        risk_strategy_context="REQ-001 risk",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context='{"test_cases": []}',
        rtm_context="REQ-001 Covered",
    )

    assert result.passed is True
    assert result.retry_count == 1
    assert result.final_review.status == FinalReviewStatus.PASS

    assert test_case_rework_service.calls == 1

    assert (
        captured["routing_result"]["routes"][0]["route"]
        == "test_case_validation"
    )

    updated_test_cases = json.loads(
        captured["updated_context"]["test_case_context"]
    )

    assert updated_test_cases["document_name"] == (
        "sample.docx"
    )

    assert updated_test_cases["test_case_summary"] == (
        "Test cases revised by Test Case workflow."
    )
