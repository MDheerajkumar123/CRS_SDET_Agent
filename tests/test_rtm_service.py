from app.rtm.services.rtm_service import RTMService


class FakeLLMResponse:
    content = """
    {
        "document_name": "SmartBank_CRS.docx",
        "rtm_summary": "Requirement traceability is complete.",
        "requirement_coverage": [
            {
                "requirement_id": "REQ-001",
                "scenario_ids": ["SCN-001"],
                "design_ids": ["TD-001"],
                "test_case_ids": ["TC-001"],
                "coverage_status": "Covered",
                "coverage_notes": "Complete traceability."
            }
        ],
        "total_requirements": 1,
        "covered_requirements": 1,
        "partially_covered_requirements": 0,
        "not_covered_requirements": 0,
        "overall_coverage_percentage": 100.0
    }
    """


class FakeLLMManager:
    def generate(self, task_name, prompt):
        assert task_name == "rtm"
        assert "REQ-001" in prompt
        assert "SCN-001" in prompt
        assert "TD-001" in prompt
        assert "TC-001" in prompt

        return FakeLLMResponse()


def test_rtm_service():
    service = RTMService(
        llm_manager=FakeLLMManager()
    )

    result = service.generate(
        document_name="SmartBank_CRS.docx",
        requirement_context="REQ-001: Valid payment.",
        scenario_context="SCN-001 → REQ-001.",
        test_design_context="TD-001 → SCN-001.",
        test_case_context="TC-001 → TD-001.",
    )

    assert result.document_name == "SmartBank_CRS.docx"
    assert len(result.requirement_coverage) == 1
    assert result.requirement_coverage[0].requirement_id == "REQ-001"
    assert result.covered_requirements == 1
    assert result.overall_coverage_percentage == 100.0

    print("RTM service validation PASS")
