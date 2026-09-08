
import json

from app.rtm.models.rtm import (
    CoverageStatus,
    RequirementCoverage,
    RTMAnalysis,
)
from app.rtm.validation.crew.rtm_validation_crew import (
    RTMValidationCrew,
)
from app.rtm.validation.models.review_result import (
    RTMReviewResult,
)


def test_rtm_validation_real():
    document_name = "CRS_Sample.docx"

    requirement_context = json.dumps(
        [
            {
                "requirement_id": "REQ-001",
                "title": "User Login",
                "description": "The system shall allow a registered user to log in.",
            },
            {
                "requirement_id": "REQ-002",
                "title": "Invalid Login",
                "description": "The system shall reject invalid login credentials.",
            },
            {
                "requirement_id": "REQ-003",
                "title": "Account Lockout",
                "description": "The system shall handle repeated failed login attempts.",
            },
        ],
        indent=2,
    )

    scenario_context = json.dumps(
        [
            {
                "scenario_id": "SCN-001",
                "requirement_id": "REQ-001",
                "title": "Valid login",
            },
            {
                "scenario_id": "SCN-002",
                "requirement_id": "REQ-002",
                "title": "Invalid credentials",
            },
            {
                "scenario_id": "SCN-003",
                "requirement_id": "REQ-003",
                "title": "Repeated failed login attempts",
            },
        ],
        indent=2,
    )

    test_design_context = json.dumps(
        [
            {
                "design_id": "TD-001",
                "scenario_id": "SCN-001",
                "requirement_id": "REQ-001",
            },
            {
                "design_id": "TD-002",
                "scenario_id": "SCN-002",
                "requirement_id": "REQ-002",
            },
            {
                "design_id": "TD-003",
                "scenario_id": "SCN-003",
                "requirement_id": "REQ-003",
            },
        ],
        indent=2,
    )

    test_case_context = json.dumps(
        [
            {
                "test_case_id": "TC-001",
                "design_id": "TD-001",
                "scenario_id": "SCN-001",
                "requirement_id": "REQ-001",
            },
            {
                "test_case_id": "TC-002",
                "design_id": "TD-002",
                "scenario_id": "SCN-002",
                "requirement_id": "REQ-002",
            },
            {
                "test_case_id": "TC-003",
                "design_id": "TD-003",
                "scenario_id": "SCN-003",
                "requirement_id": "REQ-003",
            },
        ],
        indent=2,
    )

    rtm_analysis = RTMAnalysis(
        document_name=document_name,
        rtm_summary="All three requirements are traced through the QA artifacts.",
        requirement_coverage=[
            RequirementCoverage(
                requirement_id="REQ-001",
                scenario_ids=["SCN-001"],
                design_ids=["TD-001"],
                test_case_ids=["TC-001"],
                coverage_status=CoverageStatus.COVERED,
                coverage_notes="Complete end-to-end traceability.",
            ),
            RequirementCoverage(
                requirement_id="REQ-002",
                scenario_ids=["SCN-002"],
                design_ids=["TD-002"],
                test_case_ids=["TC-002"],
                coverage_status=CoverageStatus.COVERED,
                coverage_notes="Complete end-to-end traceability.",
            ),
            RequirementCoverage(
                requirement_id="REQ-003",
                scenario_ids=["SCN-003"],
                design_ids=["TD-003"],
                test_case_ids=["TC-003"],
                coverage_status=CoverageStatus.COVERED,
                coverage_notes="Complete end-to-end traceability.",
            ),
        ],
        total_requirements=3,
        covered_requirements=3,
        partially_covered_requirements=0,
        not_covered_requirements=0,
        overall_coverage_percentage=100.0,
    )

    rtm_context = json.dumps(
        rtm_analysis.model_dump(),
        indent=2,
    )

    crew = RTMValidationCrew(
        document_name=document_name,
        requirement_context=requirement_context,
        scenario_context=scenario_context,
        test_design_context=test_design_context,
        test_case_context=test_case_context,
        rtm_context=rtm_context,
    )

    result = crew.kickoff()

    review = getattr(result, "pydantic", None)

    if review is None:
        raw = getattr(result, "raw", str(result))
        review = RTMReviewResult.model_validate_json(raw)

    assert isinstance(review, RTMReviewResult)
    assert review.status in (
        "PASS",
        "REWORK",
    )
    assert 0 <= review.score <= 100

    print(f"\nRTM validation status: {review.status}")
    print(f"RTM validation score: {review.score}")
    print(f"RTM issues: {len(review.issues)}")
    print(f"RTM required changes: {len(review.required_changes)}")

    print("REAL RTM VALIDATION EXECUTION PASS")
