import json

from app.final_review.models.review_result import (
    FinalQAReviewResult,
    FinalReviewStatus,
)
from app.final_review.services.final_qa_rework_dispatcher import (
    FinalQAReworkDispatcher,
)
from app.final_review.services.final_qa_rework_service import (
    FinalQAReworkResult,
)
from app.final_review.services.final_qa_validation_loop import (
    FinalQAValidationLoop,
)
from app.final_review.services.handlers.rtm_rework_handler import (
    RTMReworkHandler,
)
from app.rtm.models.rtm import RTMAnalysis


class FakeReviewer:
    def __init__(self):
        self.calls = 0

    def review(self, **kwargs):
        self.calls += 1

        if self.calls == 1:
            return FinalQAReviewResult(
                status=FinalReviewStatus.REWORK,
                score=70,
                issues=["RTM coverage gap"],
                required_changes=[
                    "Fix RTM coverage."
                ],
                review_summary="RTM rework required.",
            )

        return FinalQAReviewResult(
            status=FinalReviewStatus.PASS,
            score=95,
            review_summary="Approved after RTM rework.",
        )


class FakeFinalQAReworkService:
    def rework(self, request):
        return FinalQAReworkResult(
            document_name=request.document_name,
            rework_targets=[
                {
                    "artifact": "RTM",
                    "reason": "RTM coverage gap",
                    "actions": [
                        "Fix RTM coverage."
                    ],
                }
            ],
            overall_rework_summary=(
                "RTM requires rework."
            ),
        )


class FakeRTMReworkService:
    def __init__(self):
        self.calls = 0

    def rework(self, request):
        self.calls += 1

        return RTMAnalysis(
            document_name=request.document_name,
            rtm_summary=(
                "RTM revised by RTM workflow."
            ),
            requirement_coverage=[],
            total_requirements=0,
            covered_requirements=0,
            partially_covered_requirements=0,
            not_covered_requirements=0,
            overall_coverage_percentage=0.0,
        )


def test_final_qa_automatically_dispatches_rtm_rework():
    reviewer = FakeReviewer()

    final_qa_rework_service = (
        FakeFinalQAReworkService()
    )

    rtm_rework_service = FakeRTMReworkService()

    rtm_handler = RTMReworkHandler(
        rework_service=rtm_rework_service
    )

    dispatcher = FinalQAReworkDispatcher(
        requirement_handler=None,
        risk_strategy_handler=None,
        scenario_handler=None,
        test_design_handler=None,
        test_case_handler=None,
        rtm_handler=rtm_handler,
    )

    loop = FinalQAValidationLoop(
        reviewer_service=reviewer,
        rework_service=final_qa_rework_service,
        dispatcher=dispatcher,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        risk_strategy_context="REQ-001 risk",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context='{"test_cases": []}',
        rtm_context='{"requirement_coverage": []}',
    )

    assert result.passed is True
    assert result.retry_count == 1
    assert result.final_review.status == (
        FinalReviewStatus.PASS
    )

    assert rtm_rework_service.calls == 1

    # Confirm the actual RTM handler produced the
    # updated RTM context through the dispatcher.
    #
    # The FinalQAValidationLoop currently owns the
    # context internally, so the strongest observable
    # proof here is that the RTM rework service was
    # invoked exactly once through the registered handler.
