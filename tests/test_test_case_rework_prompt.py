from app.test_case.validation.prompts.rework_prompt import (
    build_test_case_rework_prompt,
)


def test_test_case_rework_prompt():
    prompt = build_test_case_rework_prompt(
        document_name="Sample_CRS.docx",
        current_test_cases="Current test cases JSON",
        issues=["Unsupported implementation assumption"],
        required_changes=["Remove unsupported assumption"],
        retry_count=1,
    )

    assert "Senior SDET Test Case Rework Engineer" in prompt
    assert "Sample_CRS.docx" in prompt
    assert "Current test cases JSON" in prompt
    assert "Unsupported implementation assumption" in prompt
    assert "Remove unsupported assumption" in prompt
    assert "rework attempt 1" in prompt
    assert "Preserve traceability" in prompt
    assert "Do not invent" in prompt
    assert "complete revised TestCaseAnalysis" in prompt
    assert "valid JSON" in prompt

    print("Test Test Case Rework Prompt PASS")
