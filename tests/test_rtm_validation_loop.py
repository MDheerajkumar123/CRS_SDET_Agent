
from app.rtm.models.rtm import (
    CoverageStatus,
    RequirementCoverage,
    RTMAnalysis,
)
from app.rtm.validation.models.review_result import (
    RTMReviewResult,
    RTMReviewStatus,
)
from app.rtm.validation.services.rtm_validation_loop import (
    RTMValidationLoop,
)


def create_rtm():
    return RTMAnalysis(
        document_name="sample.docx",
        rtm_summary="Sample RTM",
        requirement_coverage=[
            RequirementCoverage(
                requirement_id="REQ-001",
                scenario_ids=["SCN-001"],
                design_ids=["TD-001"],
                test_case_ids=["TC-001"],
                coverage_status=CoverageStatus.COVERED,
                coverage_notes="Fully traced.",
            )
        ],
        total_requirements=1,
        covered_requirements=1,
        partially_covered_requirements=0,
        not_covered_requirements=0,
        overall_coverage_percentage=100.0,
    )


class FakeValidator:
    def __init__(self, reviews):
        self.reviews = reviews
        self.index = 0

    def validate(self, **kwargs):
        review = self.reviews[self.index]
        self.index += 1
        return review


class FakeRework:
    def __init__(self):
        self.calls = 0

    def rework(self, request):
        self.calls += 1
        return create_rtm()


def test_rtm_validation_pass_path():
    validator = FakeValidator(
        [
            RTMReviewResult(
                status=RTMReviewStatus.PASS,
                score=100,
            )
        ]
    )

    rework = FakeRework()

    loop = RTMValidationLoop(
        validator_service=validator,
        rework_service=rework,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context="TC-001",
        rtm_analysis=create_rtm(),
    )

    assert result.passed is True
    assert result.retry_count == 0
    assert result.final_review.status == RTMReviewStatus.PASS
    assert rework.calls == 0


def test_rtm_validation_rework_then_pass():
    validator = FakeValidator(
        [
            RTMReviewResult(
                status=RTMReviewStatus.REWORK,
                score=70,
                issues=["Incorrect coverage"],
                required_changes=["Correct coverage"],
            ),
            RTMReviewResult(
                status=RTMReviewStatus.PASS,
                score=100,
            ),
        ]
    )

    rework = FakeRework()

    loop = RTMValidationLoop(
        validator_service=validator,
        rework_service=rework,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context="TC-001",
        rtm_analysis=create_rtm(),
    )

    assert result.passed is True
    assert result.retry_count == 1
    assert result.final_review.status == RTMReviewStatus.PASS
    assert rework.calls == 1


def test_rtm_validation_max_retry_path():
    validator = FakeValidator(
        [
            RTMReviewResult(
                status=RTMReviewStatus.REWORK,
                score=60,
                issues=["Issue"],
                required_changes=["Change"],
            ),
            RTMReviewResult(
                status=RTMReviewStatus.REWORK,
                score=65,
                issues=["Issue"],
                required_changes=["Change"],
            ),
            RTMReviewResult(
                status=RTMReviewStatus.REWORK,
                score=70,
                issues=["Issue"],
                required_changes=["Change"],
            ),
            RTMReviewResult(
                status=RTMReviewStatus.REWORK,
                score=75,
                issues=["Issue"],
                required_changes=["Change"],
            ),
        ]
    )

    rework = FakeRework()

    loop = RTMValidationLoop(
        validator_service=validator,
        rework_service=rework,
        max_retries=3,
    )

    result = loop.run(
        document_name="sample.docx",
        requirement_context="REQ-001",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context="TC-001",
        rtm_analysis=create_rtm(),
    )

    assert result.passed is False
    assert result.retry_count == 3
    assert result.final_review.status == RTMReviewStatus.REWORK
    assert rework.calls == 3
