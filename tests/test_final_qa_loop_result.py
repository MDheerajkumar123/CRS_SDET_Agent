
from app.final_review.models.loop_result import (
    FinalQAValidationLoopResult,
)
from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.final_review.models.review_result import (
    FinalQAReviewResult,
    FinalReviewStatus,
)


def test_final_qa_loop_result_pass():
    review = FinalQAReviewResult(
        status=FinalReviewStatus.PASS,
        score=100,
        review_summary="Package approved.",
    )

    result = FinalQAValidationLoopResult(
        final_review=review,
        retry_count=0,
        max_retries=3,
        passed=True,
    )

    assert result.passed is True
    assert result.retry_count == 0
    assert result.final_rework_request is None


def test_final_qa_loop_result_rework():
    review = FinalQAReviewResult(
        status=FinalReviewStatus.REWORK,
        score=70,
        issues=["Coverage gap"],
        required_changes=["Add coverage"],
        review_summary="Rework required.",
    )

    request = FinalQAReworkRequest(
        document_name="sample.docx",
        requirement_context="REQ-001",
        risk_strategy_context="REQ-001 risk",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context="TC-001",
        rtm_context="REQ-001 Partial",
        issues=["Coverage gap"],
        required_changes=["Add coverage"],
        retry_count=1,
    )

    result = FinalQAValidationLoopResult(
        final_review=review,
        final_rework_request=request,
        retry_count=1,
        max_retries=3,
        passed=False,
    )

    assert result.passed is False
    assert result.retry_count == 1
    assert result.final_rework_request is not None
    assert result.final_rework_request.document_name == "sample.docx"
