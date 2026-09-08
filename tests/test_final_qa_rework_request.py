
from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)


def test_final_qa_rework_request():
    request = FinalQAReworkRequest(
        document_name="sample.docx",
        requirement_context="REQ-001: Login",
        risk_strategy_context="REQ-001: High risk",
        scenario_context="SCN-001: Valid login",
        test_design_context="TD-001: Login design",
        test_case_context="TC-001: Login test",
        rtm_context="REQ-001: Covered",
        issues=["Security coverage is missing."],
        required_changes=[
            "Add appropriate security coverage."
        ],
        retry_count=1,
    )

    assert request.document_name == "sample.docx"
    assert request.retry_count == 1
    assert "Security coverage is missing." in request.issues
    assert (
        "Add appropriate security coverage."
        in request.required_changes
    )
