
from app.rtm.prompts.rtm import build_rtm_prompt


def test_build_rtm_prompt():
    prompt = build_rtm_prompt(
        document_name="SmartBank_CRS.docx",
        requirement_context="REQ-001: Valid payment must succeed.",
        scenario_context="SCN-001 → REQ-001: Successful payment.",
        test_design_context="TD-001 → SCN-001: Positive payment design.",
        test_case_context="TC-001 → TD-001: Verify successful payment.",
    )

    assert "SmartBank_CRS.docx" in prompt
    assert "REQ-001" in prompt
    assert "SCN-001" in prompt
    assert "TD-001" in prompt
    assert "TC-001" in prompt

    assert "Covered" in prompt
    assert "Partial" in prompt
    assert "Not Covered" in prompt

    assert "Do not invent requirement IDs" in prompt
    assert "Do not invent scenario IDs" in prompt
    assert "Do not invent design IDs" in prompt
    assert "Do not invent test case IDs" in prompt

    assert "overall_coverage_percentage" in prompt

    print("RTM prompt builder validation PASS")
