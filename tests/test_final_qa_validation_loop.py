from app.final_review.models.review_result import (
    FinalQAReviewResult,
    FinalReviewStatus,
)
from app.final_review.services.final_qa_validation_loop import (
    FinalQAValidationLoop,
)
from app.final_review.services.final_qa_rework_service import (
    FinalQAReworkResult,
    ReworkTarget,
)


class FakeReviewer:
    def __init__(self, reviews):
        self.reviews = reviews
        self.index = 0

    def review(self, **kwargs):
        review = self.reviews[self.index]
        self.index += 1
        return review


class FakeRework:
    def __init__(self, artifact="TEST_CASES"):
        self.calls = 0
        self.artifact = artifact

    def rework(self, request):
        self.calls += 1

        if self.artifact == "RTM":
            return FinalQAReworkResult(
                document_name=request.document_name,
                rework_targets=[
                    ReworkTarget(
                        artifact="RTM",
                        reason="RTM coverage gap",
                        actions=["Fix RTM coverage."],
                    )
                ],
                overall_rework_summary="RTM requires rework.",
            )

        return FinalQAReworkResult(
            document_name=request.document_name,
            rework_targets=[
                ReworkTarget(
                    artifact="TEST_CASES",
                    reason="Coverage gap",
                    actions=["Add required coverage."],
                )
            ],
            overall_rework_summary="Test cases require rework.",
        )


def test_final_qa_validation_loop_pass_path():
    reviewer = FakeReviewer(
        [
            FinalQAReviewResult(
                status=FinalReviewStatus.PASS,
                score=100,
                review_summary="Approved.",
            )
        ]
    )

    rework = FakeRework()

    loop = FinalQAValidationLoop(
        reviewer_service=reviewer,
        rework_service=rework,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        risk_strategy_context="REQ-001 risk",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context="TC-001",
        rtm_context="REQ-001 Covered",
    )

    assert result.passed is True
    assert result.retry_count == 0
    assert result.final_review.status == FinalReviewStatus.PASS
    assert rework.calls == 0


def test_final_qa_validation_loop_rework_requires_handler():
    reviewer = FakeReviewer(
        [
            FinalQAReviewResult(
                status=FinalReviewStatus.REWORK,
                score=70,
                issues=["Coverage gap"],
                required_changes=["Add coverage."],
                review_summary="Rework required.",
            )
        ]
    )

    rework = FakeRework()

    loop = FinalQAValidationLoop(
        reviewer_service=reviewer,
        rework_service=rework,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        risk_strategy_context="REQ-001 risk",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context="TC-001",
        rtm_context="REQ-001 Covered",
    )

    assert result.passed is False
    assert result.retry_count == 1
    assert result.final_rework_request is not None
    assert rework.calls == 1


def test_final_qa_validation_loop_rework_then_pass():
    reviewer = FakeReviewer(
        [
            FinalQAReviewResult(
                status=FinalReviewStatus.REWORK,
                score=70,
                issues=["Coverage gap"],
                required_changes=["Add coverage."],
                review_summary="Rework required.",
            ),
            FinalQAReviewResult(
                status=FinalReviewStatus.PASS,
                score=95,
                review_summary="Approved after rework.",
            ),
        ]
    )

    rework = FakeRework()

    def rework_handler(
        request,
        rework_result,
        routing_result,
        current_context,
    ):
        updated = dict(current_context)

        updated["test_case_context"] = (
            current_context["test_case_context"]
            + "\nREWORKED"
        )

        return updated

    loop = FinalQAValidationLoop(
        reviewer_service=reviewer,
        rework_service=rework,
        rework_handler=rework_handler,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        risk_strategy_context="REQ-001 risk",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context="TC-001",
        rtm_context="REQ-001 Covered",
    )

    assert result.passed is True
    assert result.retry_count == 1
    assert result.final_review.status == FinalReviewStatus.PASS
    assert rework.calls == 1


def test_final_qa_validation_loop_max_retry():
    reviewer = FakeReviewer(
        [
            FinalQAReviewResult(
                status=FinalReviewStatus.REWORK,
                score=60,
                issues=["Issue"],
                required_changes=["Change"],
            ),
            FinalQAReviewResult(
                status=FinalReviewStatus.REWORK,
                score=65,
                issues=["Issue"],
                required_changes=["Change"],
            ),
            FinalQAReviewResult(
                status=FinalReviewStatus.REWORK,
                score=70,
                issues=["Issue"],
                required_changes=["Change"],
            ),
            FinalQAReviewResult(
                status=FinalReviewStatus.REWORK,
                score=75,
                issues=["Issue"],
                required_changes=["Change"],
            ),
        ]
    )

    rework = FakeRework()

    def rework_handler(
        request,
        rework_result,
        routing_result,
        current_context,
    ):
        return dict(current_context)

    loop = FinalQAValidationLoop(
        reviewer_service=reviewer,
        rework_service=rework,
        rework_handler=rework_handler,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        risk_strategy_context="REQ-001 risk",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context="TC-001",
        rtm_context="REQ-001 Covered",
    )

    assert result.passed is False
    assert result.retry_count == 3
    assert result.final_review.status == FinalReviewStatus.REWORK
    assert result.final_rework_request is not None
    assert rework.calls == 3


def test_final_qa_validation_loop_routes_test_cases_to_correct_handler():
    reviewer = FakeReviewer(
        [
            FinalQAReviewResult(
                status=FinalReviewStatus.REWORK,
                score=70,
                issues=["Test case coverage gap"],
                required_changes=["Add missing test case coverage."],
                review_summary="Test case rework required.",
            ),
            FinalQAReviewResult(
                status=FinalReviewStatus.PASS,
                score=95,
                review_summary="Approved after test case rework.",
            ),
        ]
    )

    rework = FakeRework(artifact="TEST_CASES")

    captured = {}

    def rework_handler(
        request,
        rework_result,
        routing_result,
        current_context,
    ):
        captured["routing_result"] = routing_result
        captured["current_context"] = dict(current_context)

        assert len(routing_result["routes"]) == 1

        route = routing_result["routes"][0]

        assert route["artifact"] == "TEST_CASES"
        assert route["route"] == "test_case_validation"

        updated = dict(current_context)

        updated["test_case_context"] = (
            current_context["test_case_context"]
            + "\nREWORKED"
        )

        return updated

    loop = FinalQAValidationLoop(
        reviewer_service=reviewer,
        rework_service=rework,
        rework_handler=rework_handler,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        risk_strategy_context="REQ-001 risk",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context="TC-001",
        rtm_context="REQ-001 Covered",
    )

    assert result.passed is True
    assert result.retry_count == 1
    assert result.final_review.status == FinalReviewStatus.PASS

    assert captured["routing_result"]["routes"][0]["artifact"] == (
        "TEST_CASES"
    )

    assert captured["routing_result"]["routes"][0]["route"] == (
        "test_case_validation"
    )

    assert captured["current_context"]["test_case_context"] == (
        "TC-001"
    )


def test_final_qa_validation_loop_routes_rtm_to_correct_handler():
    reviewer = FakeReviewer(
        [
            FinalQAReviewResult(
                status=FinalReviewStatus.REWORK,
                score=70,
                issues=["RTM coverage gap"],
                required_changes=["Fix RTM coverage."],
                review_summary="RTM rework required.",
            ),
            FinalQAReviewResult(
                status=FinalReviewStatus.PASS,
                score=95,
                review_summary="Approved after RTM rework.",
            ),
        ]
    )

    rework = FakeRework(artifact="RTM")

    captured = {}

    def rework_handler(
        request,
        rework_result,
        routing_result,
        current_context,
    ):
        captured["routing_result"] = routing_result
        captured["current_context"] = dict(current_context)

        assert len(routing_result["routes"]) == 1

        route = routing_result["routes"][0]

        assert route["artifact"] == "RTM"
        assert route["route"] == "rtm_validation"

        updated = dict(current_context)

        updated["rtm_context"] = (
            current_context["rtm_context"]
            + "\nREWORKED"
        )

        return updated

    loop = FinalQAValidationLoop(
        reviewer_service=reviewer,
        rework_service=rework,
        rework_handler=rework_handler,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        risk_strategy_context="REQ-001 risk",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context="TC-001",
        rtm_context="REQ-001 Covered",
    )

    assert result.passed is True
    assert result.retry_count == 1
    assert result.final_review.status == FinalReviewStatus.PASS

    assert captured["routing_result"]["routes"][0]["artifact"] == (
        "RTM"
    )

    assert captured["routing_result"]["routes"][0]["route"] == (
        "rtm_validation"
    )

    assert captured["current_context"]["rtm_context"] == (
        "REQ-001 Covered"
    )
