
from app.rtm.validation.prompts.rework_prompt import (
    build_rtm_rework_prompt,
)


def test_build_rtm_rework_prompt():
    prompt = build_rtm_rework_prompt(
        document_name="sample.docx",
        current_rtm='{"requirement_id": "REQ-001"}',
        issues=["Incorrect coverage"],
        required_changes=["Correct coverage classification"],
        retry_count=1,
    )

    assert "REQ-001" in prompt
    assert "Incorrect coverage" in prompt
    assert "Correct coverage classification" in prompt
    assert "Do not invent requirement IDs" in prompt
    assert "Do not invent scenario IDs" in prompt
    assert "Do not invent test design IDs" in prompt
    assert "Do not invent test case IDs" in prompt
    assert "complete RTMAnalysis" in prompt
