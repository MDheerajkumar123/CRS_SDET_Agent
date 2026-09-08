
from types import SimpleNamespace

from app.rtm.models.rtm import (
    CoverageStatus,
    RequirementCoverage,
    RTMAnalysis,
)
from app.rtm.validation.models.rework_request import (
    RTMReworkRequest,
)
from app.rtm.validation.services.rtm_rework_service import (
    RTMReworkService,
)


class FakeLLMManager:
    def generate(self, task_name, prompt):
        assert task_name == "rtm"
        assert "Correct coverage" in prompt

        return SimpleNamespace(
            content="""
            {
                "document_name": "sample.docx",
                "rtm_summary": "Coverage corrected after review.",
                "requirement_coverage": [
                    {
                        "requirement_id": "REQ-001",
                        "scenario_ids": ["SCN-001"],
                        "design_ids": ["TD-001"],
                        "test_case_ids": ["TC-001"],
                        "coverage_status": "Covered",
                        "coverage_notes": "Complete traceability."
                    }
                ],
                "total_requirements": 1,
                "covered_requirements": 1,
                "partially_covered_requirements": 0,
                "not_covered_requirements": 0,
                "overall_coverage_percentage": 100.0
            }
            """
        )


def test_rtm_rework_service():
    request = RTMReworkRequest(
        document_name="sample.docx",
        current_rtm='{"requirement_id": "REQ-001"}',
        issues=["Incorrect coverage"],
        required_changes=["Correct coverage"],
        retry_count=1,
    )

    service = RTMReworkService(
        llm_manager=FakeLLMManager()
    )

    result = service.rework(request)

    assert isinstance(result, RTMAnalysis)
    assert result.document_name == "sample.docx"
    assert len(result.requirement_coverage) == 1
    assert (
        result.requirement_coverage[0].coverage_status
        == CoverageStatus.COVERED
    )
    assert result.overall_coverage_percentage == 100.0
