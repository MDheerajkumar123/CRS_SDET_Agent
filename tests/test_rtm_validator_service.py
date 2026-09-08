
from types import SimpleNamespace

from app.rtm.models.rtm import (
    CoverageStatus,
    RequirementCoverage,
    RTMAnalysis,
)
from app.rtm.validation.models.review_result import (
    RTMReviewStatus,
)
from app.rtm.validation.services.rtm_validator_service import (
    RTMValidatorService,
)


class FakeLLMManager:
    def generate(self, task_name, prompt):
        assert task_name == "rtm_validator"
        assert "RTM" in prompt

        return SimpleNamespace(
            content="""
            {
                "status": "PASS",
                "score": 95,
                "issues": [],
                "required_changes": []
            }
            """
        )


def test_rtm_validator_service():
    rtm_analysis = RTMAnalysis(
        document_name="sample.docx",
        rtm_summary="All requirements were evaluated.",
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

    service = RTMValidatorService(
        llm_manager=FakeLLMManager()
    )

    result = service.validate(
        document_name="sample.docx",
        requirement_context="REQ-001: Login requirement",
        scenario_context="SCN-001: Valid login",
        test_design_context="TD-001: Login design",
        test_case_context="TC-001: Verify valid login",
        rtm_analysis=rtm_analysis,
    )

    assert result.status == RTMReviewStatus.PASS
    assert result.score == 95
    assert result.issues == []
    assert result.required_changes == []
