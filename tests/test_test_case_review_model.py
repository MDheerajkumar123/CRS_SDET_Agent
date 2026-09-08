from app.test_case.models.review_result import (
    TestCaseReviewResult,
    TestCaseReviewStatus,
)


def test_test_case_review_model():
    result = TestCaseReviewResult(
        status=TestCaseReviewStatus.PASS,
        score=95,
        issues=[],
        required_changes=[],
    )

    assert result.status == TestCaseReviewStatus.PASS
    assert result.score == 95
    assert result.issues == []
    assert result.required_changes == []

    print("Test Test Case Review Model PASS")
