from app.test_case.prompts.test_case import build_test_case_prompt
from app.test_case.validation.prompts.rework_prompt import (
    build_test_case_rework_prompt,
)


def test_test_case_prompt_requires_source_faithful_pairwise_and_security_guidance():
    prompt = build_test_case_prompt(
        document_name="generic-crs.docx",
        requirement_context="A security control is required.",
        risk_strategy_context="Security testing is recommended.",
        scenario_context="Verify documented security behavior.",
        test_design_context=(
            "Technique: Pairwise. Defined combinations: OS version x "
            "device type x payment method."
        ),
    )

    assert "reusable procedure must be executed once" in prompt
    assert "Do not infer or create a matrix" in prompt
    assert "Preserve a named tool, product, or platform mechanism" in prompt
    assert "network traffic capture tool" in prompt
    assert "Security/Ops team" in prompt
    assert "Do not invent algorithms, key lengths" in prompt


def test_test_case_rework_prompt_preserves_pairwise_and_evidence_dependencies():
    prompt = build_test_case_rework_prompt(
        document_name="generic-crs.docx",
        current_test_cases="Current cases reference Pairwise test data.",
        issues=["Coverage is incomplete."],
        required_changes=["Address the missing coverage."],
        retry_count=1,
    )

    assert "every combination explicitly" in prompt
    assert "generic capability language" in prompt
    assert "manual evidence-review step" in prompt
