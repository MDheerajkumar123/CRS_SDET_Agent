from app.rtm.models.rtm import (
    CoverageStatus,
    RequirementCoverage,
    RTMAnalysis,
)


def test_rtm_model():
    coverage = RequirementCoverage(
        requirement_id="REQ-001",
        scenario_ids=["SCN-001"],
        design_ids=["TD-001"],
        test_case_ids=["TC-001"],
        coverage_status=CoverageStatus.COVERED,
        coverage_notes="Requirement is fully traceable.",
    )

    analysis = RTMAnalysis(
        document_name="SmartBank_CRS.docx",
        rtm_summary="Requirement traceability is established.",
        requirement_coverage=[coverage],
        total_requirements=1,
        covered_requirements=1,
        partially_covered_requirements=0,
        not_covered_requirements=0,
        overall_coverage_percentage=100.0,
    )

    assert analysis.document_name == "SmartBank_CRS.docx"
    assert len(analysis.requirement_coverage) == 1
    assert analysis.requirement_coverage[0].requirement_id == "REQ-001"
    assert analysis.covered_requirements == 1
    assert analysis.overall_coverage_percentage == 100.0

    print("RTM model validation PASS")
