
import json

from app.rtm.models.rtm import (
    CoverageStatus,
    RequirementCoverage,
    RTMAnalysis,
)
from app.rtm.validation.services.rtm_validation_loop import (
    RTMValidationLoop,
)


def test_rtm_validation_loop_real():
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
        rtm_summary="Initial RTM requiring validation.",
        requirement_coverage=[
            RequirementCoverage(
                requirement_id="REQ-001",
                scenario_ids=["SCN-001"],
                design_ids=["TD-001"],
                test_case_ids=["TC-001"],
                coverage_status=CoverageStatus.COVERED,
                coverage_notes="Complete traceability.",
            ),
            RequirementCoverage(
                requirement_id="REQ-002",
                scenario_ids=["SCN-002"],
                design_ids=["TD-002"],
                test_case_ids=["TC-002"],
                coverage_status=CoverageStatus.COVERED,
                coverage_notes="Complete traceability.",
            ),
            RequirementCoverage(
                requirement_id="REQ-003",
                scenario_ids=["SCN-003"],
                design_ids=["TD-003"],
                test_case_ids=["TC-003"],
                coverage_status=CoverageStatus.COVERED,
                coverage_notes="Complete traceability.",
            ),
        ],
        total_requirements=3,
        covered_requirements=3,
        partially_covered_requirements=0,
        not_covered_requirements=0,
        overall_coverage_percentage=100.0,
    )

    loop = RTMValidationLoop(max_retries=3)

    result = loop.run(
        document_name=document_name,
        requirement_context=requirement_context,
        scenario_context=scenario_context,
        test_design_context=test_design_context,
        test_case_context=test_case_context,
        rtm_analysis=rtm_analysis,
    )

    print(f"\nFinal RTM validation status: {result.final_review.status}")
    print(f"Final RTM validation score: {result.final_review.score}")
    print(f"Retry count: {result.retry_count}")
    print(f"Maximum retries: {result.max_retries}")
    print(f"Passed: {result.passed}")

    print(
        f"Final covered requirements: "
        f"{result.final_rtm.covered_requirements}"
    )
    print(
        f"Final partial requirements: "
        f"{result.final_rtm.partially_covered_requirements}"
    )
    print(
        f"Final not covered requirements: "
        f"{result.final_rtm.not_covered_requirements}"
    )
    print(
        f"Final coverage: "
        f"{result.final_rtm.overall_coverage_percentage}%"
    )

    assert result.final_rtm is not None
    assert result.final_review is not None
    assert result.retry_count <= 3

    print("REAL RTM VALIDATION LOOP PASS")
