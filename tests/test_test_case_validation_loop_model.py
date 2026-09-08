from app.test_case.models.review_result import (
    TestCaseReviewResult,
    TestCaseReviewStatus,
)
from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.validation.models.loop_result import (
    TestCaseValidationLoopResult,
)


def test_test_case_validation_loop_result():
    test_cases = TestCaseAnalysis(
        document_name="Sample_CRS.docx",
        test_case_summary="Validated test cases",
        test_cases=[],
        overall_test_case_confidence=0.95,
    )

    review = TestCaseReviewResult(
        status=TestCaseReviewStatus.PASS,
        score=95,
        issues=[],
        required_changes=[],
    )

    result = TestCaseValidationLoopResult(
        final_test_cases=test_cases,
        final_review=review,
        retry_count=0,
        max_retries=3,
        passed=True,
    )

    assert result.final_test_cases == test_cases
    assert result.final_review == review
    assert result.retry_count == 0
    assert result.max_retries == 3
    assert result.passed is True

    print("Test Test Case Validation Loop Result Model PASS")
