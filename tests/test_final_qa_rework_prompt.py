
from app.final_review.prompts.rework_prompt import (
    build_final_qa_rework_prompt,
)


def test_build_final_qa_rework_prompt():
    prompt = build_final_qa_rework_prompt(
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

    assert "REQ-001: Login" in prompt
    assert "REQ-001: High risk" in prompt
    assert "SCN-001: Valid login" in prompt
    assert "TD-001: Login design" in prompt
    assert "TC-001: Login test" in prompt
    assert "REQ-001: Covered" in prompt

    assert "Security coverage is missing." in prompt
    assert "Add appropriate security coverage." in prompt

    assert "Do not invent requirements" in prompt
    assert "Do not invent requirement IDs" in prompt
    assert "Do not invent scenario IDs" in prompt
    assert "Do not invent test design IDs" in prompt
    assert "Do not invent test case IDs" in prompt
    assert "Do not inflate coverage percentages" in prompt

    assert "REQUIREMENTS" in prompt
    assert "RISK_STRATEGY" in prompt
    assert "SCENARIOS" in prompt
    assert "TEST_DESIGNS" in prompt
    assert "TEST_CASES" in prompt
    assert "RTM" in prompt

    assert "rework_targets" in prompt
    assert "overall_rework_summary" in prompt
    assert "valid JSON only" in prompt
