from app.final_review.models.review_result import (
    FinalQAReviewResult,
    FinalReviewStatus,
)


def test_final_qa_review_pass():
    result = FinalQAReviewResult(
        status=FinalReviewStatus.PASS,
        score=100,
        review_summary="QA package is ready for final delivery.",
    )

    assert result.status == FinalReviewStatus.PASS
    assert result.score == 100
    assert result.issues == []
    assert result.required_changes == []


def test_final_qa_review_rework():
    result = FinalQAReviewResult(
        status=FinalReviewStatus.REWORK,
        score=70,
        issues=["Incomplete traceability"],
        required_changes=["Correct RTM coverage"],
        review_summary="Rework is required.",
    )

    assert result.status == FinalReviewStatus.REWORK
    assert result.score == 70
    assert "Incomplete traceability" in result.issues
    assert "Correct RTM coverage" in result.required_changes
