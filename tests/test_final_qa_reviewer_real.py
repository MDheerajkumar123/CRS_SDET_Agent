
import json

from app.final_review.crew.final_qa_reviewer_crew import (
    FinalQAReviewerCrew,
)
from app.final_review.models.review_result import (
    FinalQAReviewResult,
    FinalReviewStatus,
)


def test_final_qa_reviewer_real():
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
        ],
        indent=2,
    )

    risk_strategy_context = json.dumps(
        [
            {
                "requirement_id": "REQ-001",
                "risk_level": "High",
                "risk_score": 80,
                "risk_reason": "Authentication is business critical.",
                "recommended_test_types": [
                    "Functional",
                    "Negative",
                    "Security",
                ],
            },
            {
                "requirement_id": "REQ-002",
                "risk_level": "High",
                "risk_score": 75,
                "risk_reason": "Invalid authentication must be handled correctly.",
                "recommended_test_types": [
                    "Negative",
                    "Security",
                ],
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
                "scenario_type": "Positive",
            },
            {
                "scenario_id": "SCN-002",
                "requirement_id": "REQ-002",
                "title": "Invalid credentials",
                "scenario_type": "Negative",
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
                "technique": "Use Case",
            },
            {
                "design_id": "TD-002",
                "scenario_id": "SCN-002",
                "requirement_id": "REQ-002",
                "technique": "Error Guessing",
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
                "test_type": "Functional",
                "steps": [
                    "Enter valid credentials.",
                    "Submit the login request.",
                ],
                "expected_results": [
                    "The registered user is authenticated successfully."
                ],
            },
            {
                "test_case_id": "TC-002",
                "design_id": "TD-002",
                "scenario_id": "SCN-002",
                "requirement_id": "REQ-002",
                "test_type": "Negative",
                "steps": [
                    "Enter invalid credentials.",
                    "Submit the login request.",
                ],
                "expected_results": [
                    "The login request is rejected."
                ],
            },
        ],
        indent=2,
    )

    rtm_context = json.dumps(
        {
            "document_name": document_name,
            "requirement_coverage": [
                {
                    "requirement_id": "REQ-001",
                    "scenario_ids": ["SCN-001"],
                    "design_ids": ["TD-001"],
                    "test_case_ids": ["TC-001"],
                    "coverage_status": "Covered",
                    "coverage_notes": "Complete traceability.",
                },
                {
                    "requirement_id": "REQ-002",
                    "scenario_ids": ["SCN-002"],
                    "design_ids": ["TD-002"],
                    "test_case_ids": ["TC-002"],
                    "coverage_status": "Covered",
                    "coverage_notes": "Complete traceability.",
                },
            ],
            "total_requirements": 2,
            "covered_requirements": 2,
            "partially_covered_requirements": 0,
            "not_covered_requirements": 0,
            "overall_coverage_percentage": 100.0,
        },
        indent=2,
    )

    crew = FinalQAReviewerCrew(
        document_name=document_name,
        requirement_context=requirement_context,
        risk_strategy_context=risk_strategy_context,
        scenario_context=scenario_context,
        test_design_context=test_design_context,
        test_case_context=test_case_context,
        rtm_context=rtm_context,
    )

    result = crew.kickoff()

    review = getattr(result, "pydantic", None)

    if review is None:
        raw = getattr(result, "raw", str(result))
        review = FinalQAReviewResult.model_validate_json(raw)

    assert isinstance(review, FinalQAReviewResult)
    assert review.status in (
        FinalReviewStatus.PASS,
        FinalReviewStatus.REWORK,
    )
    assert 0 <= review.score <= 100

    print(f"\nFinal QA status: {review.status}")
    print(f"Final QA score: {review.score}")
    print(f"Final QA issues: {len(review.issues)}")
    print(
        f"Final QA required changes: "
        f"{len(review.required_changes)}"
    )
    print(f"Review summary: {review.review_summary}")

    print("REAL FINAL QA REVIEW EXECUTION PASS")
