from app.test_case.models.review_result import (
    TestCaseReviewResult,
    TestCaseReviewStatus,
)
from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.validation.models.loop_result import (
    TestCaseValidationLoopResult,
)
from app.test_case.validation.services.test_case_validation_loop import (
    TestCaseValidationLoop,
)


def create_test_cases():
    return TestCaseAnalysis(
        document_name="Sample_CRS.docx",
        test_case_summary="Test cases",
        test_cases=[],
        overall_test_case_confidence=0.90,
    )


class MockValidator:
    def __init__(self, reviews):
        self.reviews = reviews
        self.call_count = 0

    def validate(self, **kwargs):
        review = self.reviews[self.call_count]
        self.call_count += 1
        return review


class MockRework:
    def __init__(self):
        self.call_count = 0

    def rework(self, request):
        self.call_count += 1
        return create_test_cases()


def test_validation_loop_pass_first_attempt():
    validator = MockValidator(
        [
            TestCaseReviewResult(
                status=TestCaseReviewStatus.PASS,
                score=95,
            )
        ]
    )
    rework = MockRework()

    loop = TestCaseValidationLoop(
        validator_service=validator,
        rework_service=rework,
        max_retries=3,
    )

    result = loop.run(
        document_name="Sample_CRS.docx",
        requirement_context="Requirements",
        risk_strategy_context="Risk",
        scenario_context="Scenarios",
        test_design_context="Designs",
        test_case_analysis=create_test_cases(),
    )

    assert isinstance(result, TestCaseValidationLoopResult)
    assert result.passed is True
    assert result.retry_count == 0
    assert result.final_review.status == TestCaseReviewStatus.PASS
    assert rework.call_count == 0

    print("PASS: Test Case validation PASS path")


def test_validation_loop_rework_then_pass():
    validator = MockValidator(
        [
            TestCaseReviewResult(
                status=TestCaseReviewStatus.REWORK,
                score=70,
                issues=["Unsupported assumption"],
                required_changes=["Remove assumption"],
            ),
            TestCaseReviewResult(
                status=TestCaseReviewStatus.PASS,
                score=95,
            ),
        ]
    )
    rework = MockRework()

    loop = TestCaseValidationLoop(
        validator_service=validator,
        rework_service=rework,
        max_retries=3,
    )

    result = loop.run(
        document_name="Sample_CRS.docx",
        requirement_context="Requirements",
        risk_strategy_context="Risk",
        scenario_context="Scenarios",
        test_design_context="Designs",
        test_case_analysis=create_test_cases(),
    )

    assert result.passed is True
    assert result.retry_count == 1
    assert result.final_review.status == TestCaseReviewStatus.PASS
    assert rework.call_count == 1

    print("PASS: Test Case validation REWORK → PASS path")


def test_validation_loop_max_retries():
    validator = MockValidator(
        [
            TestCaseReviewResult(
                status=TestCaseReviewStatus.REWORK,
                score=60,
                issues=["Issue"],
                required_changes=["Change"],
            ),
            TestCaseReviewResult(
                status=TestCaseReviewStatus.REWORK,
                score=60,
                issues=["Issue"],
                required_changes=["Change"],
            ),
            TestCaseReviewResult(
                status=TestCaseReviewStatus.REWORK,
                score=60,
                issues=["Issue"],
                required_changes=["Change"],
            ),
            TestCaseReviewResult(
                status=TestCaseReviewStatus.REWORK,
                score=60,
                issues=["Issue"],
                required_changes=["Change"],
            ),
        ]
    )
    rework = MockRework()

    loop = TestCaseValidationLoop(
        validator_service=validator,
        rework_service=rework,
        max_retries=3,
    )

    result = loop.run(
        document_name="Sample_CRS.docx",
        requirement_context="Requirements",
        risk_strategy_context="Risk",
        scenario_context="Scenarios",
        test_design_context="Designs",
        test_case_analysis=create_test_cases(),
    )

    assert result.passed is False
    assert result.retry_count == 3
    assert result.final_review.status == TestCaseReviewStatus.REWORK
    assert rework.call_count == 3

    print("PASS: Test Case validation maximum retry path")
