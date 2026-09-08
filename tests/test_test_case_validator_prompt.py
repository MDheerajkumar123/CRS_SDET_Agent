from app.test_case.validation.prompts.test_case_validator import (
    build_test_case_validator_prompt,
)


def test_test_case_validator_prompt():
    prompt = build_test_case_validator_prompt(
        document_name="Sample_CRS.docx",
        requirement_context="Requirement context",
        risk_strategy_context="Risk strategy context",
        scenario_context="Scenario context",
        test_design_context="Test design context",
        test_case_context="Test case context",
    )

    assert "Senior SDET Test Case Validation Reviewer" in prompt
    assert "TRACEABILITY" in prompt
    assert "SOURCE FIDELITY" in prompt
    assert "TEST CASE COMPLETENESS" in prompt
    assert "TEST STEPS" in prompt
    assert "EXPECTED RESULTS" in prompt
    assert "RISK ALIGNMENT" in prompt
    assert "COVERAGE" in prompt
    assert "DUPLICATES" in prompt
    assert "TESTABILITY" in prompt
    assert "PASS" in prompt
    assert "REWORK" in prompt
    assert "valid JSON" in prompt
    assert "TestCase" not in prompt

    print("Test Test Case Validator Prompt PASS")
