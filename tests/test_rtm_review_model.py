
from app.rtm.validation.models.review_result import (
    RTMReviewResult,
    RTMReviewStatus,
)


def test_rtm_review_result_pass():
    result = RTMReviewResult(
        status=RTMReviewStatus.PASS,
        score=95,
        issues=[],
        required_changes=[],
    )

    assert result.status == RTMReviewStatus.PASS
    assert result.score == 95
    assert result.issues == []
    assert result.required_changes == []

    print("RTM review PASS model validation PASS")


def test_rtm_review_result_rework():
    result = RTMReviewResult(
        status=RTMReviewStatus.REWORK,
        score=70,
        issues=["Missing requirement coverage."],
        required_changes=["Add missing traceability."],
    )

    assert result.status == RTMReviewStatus.REWORK
    assert result.score == 70
    assert len(result.issues) == 1
    assert len(result.required_changes) == 1

    print("RTM review REWORK model validation PASS")
