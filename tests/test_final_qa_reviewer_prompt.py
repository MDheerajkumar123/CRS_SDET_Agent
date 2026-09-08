
from app.final_review.prompts.final_qa_reviewer import (
    build_final_qa_reviewer_prompt,
)


def test_build_final_qa_reviewer_prompt():
    prompt = build_final_qa_reviewer_prompt(
        document_name="sample.docx",
        requirement_context="REQ-001: Login",
        risk_strategy_context="REQ-001: High risk",
        scenario_context="SCN-001: Valid login",
        test_design_context="TD-001: Login design",
        test_case_context="TC-001: Login test",
        rtm_context="REQ-001: Covered",
    )

    assert "REQ-001: Login" in prompt
    assert "REQ-001: High risk" in prompt
    assert "SCN-001: Valid login" in prompt
    assert "TD-001: Login design" in prompt
    assert "TC-001: Login test" in prompt
    assert "REQ-001: Covered" in prompt

    assert "REQUIREMENT COMPLETENESS" in prompt
    assert "RISK AND TEST STRATEGY" in prompt
    assert "SCENARIO COVERAGE" in prompt
    assert "TEST DESIGN QUALITY" in prompt
    assert "TEST CASE QUALITY" in prompt
    assert "RTM QUALITY" in prompt
    assert "CROSS-ARTIFACT CONSISTENCY" in prompt
    assert "HALLUCINATION PREVENTION" in prompt
    assert "V1 SCOPE" in prompt
    assert "FINAL DELIVERY READINESS" in prompt

    assert "PASS | REWORK" in prompt
    assert "0 to 100" in prompt
    assert "valid JSON only" in prompt
