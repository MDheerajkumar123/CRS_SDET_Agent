
from app.test_design.models.test_design import (
    TestDesignAnalysis,
)
from app.test_design.services.test_design_rework_service import (
    TestDesignReworkService,
)


class FakeLLMResponse:
    def __init__(self, content):
        self.content = content


class FakeLLMManager:
    def __init__(self, content):
        self.content = content
        self.received_task_name = None
        self.received_prompt = None

    def generate(self, task_name, prompt):
        self.received_task_name = task_name
        self.received_prompt = prompt

        return FakeLLMResponse(self.content)


def valid_design_json():
    return """
    {
      "document_name": "sample.docx",
      "design_summary": "Reworked test design.",
      "test_designs": [
        {
          "design_id": "TD-001",
          "scenario_id": "SCN-001",
          "requirement_id": "REQ-001",
          "title": "Validate supported scenario",
          "objective": "Verify the supported scenario behavior.",
          "test_design_technique": "Equivalence Partitioning",
          "test_data_conditions": [
            "Use valid data supported by the CRS."
          ],
          "coverage_area": "Requirement behavior",
          "expected_focus": "Verify the expected scenario behavior.",
          "source_scenario": "SCN-001"
        }
      ],
      "overall_design_confidence": 0.9
    }
    """


def test_test_design_rework_service_returns_test_design_analysis():
    fake_llm = FakeLLMManager(valid_design_json())

    service = TestDesignReworkService(
        llm_manager=fake_llm
    )

    result = service.rework(
        document_name="sample.docx",
        requirement_context="Requirement ID: REQ-001",
        risk_strategy_context="Requirement ID: REQ-001\nRisk Level: High",
        scenario_context="Scenario ID: SCN-001",
        current_design_context='{"test_designs": []}',
        issues=["Design traceability needs correction."],
        required_changes=["Correct scenario linkage."],
        retry_count=1,
    )

    assert isinstance(result, TestDesignAnalysis)
    assert result.document_name == "sample.docx"
    assert len(result.test_designs) == 1
    assert result.test_designs[0].design_id == "TD-001"
    assert result.test_designs[0].scenario_id == "SCN-001"
    assert result.test_designs[0].requirement_id == "REQ-001"
    assert result.overall_design_confidence == 0.9


def test_test_design_rework_service_uses_correct_llm_task():
    fake_llm = FakeLLMManager(valid_design_json())

    service = TestDesignReworkService(
        llm_manager=fake_llm
    )

    service.rework(
        document_name="sample.docx",
        requirement_context="Requirement ID: REQ-001",
        risk_strategy_context="Risk Level: High",
        scenario_context="Scenario ID: SCN-001",
        current_design_context='{"test_designs": []}',
        issues=["Issue 1"],
        required_changes=["Change 1"],
        retry_count=2,
    )

    assert fake_llm.received_task_name == "test_design"
    assert fake_llm.received_prompt is not None
    assert "sample.docx" in fake_llm.received_prompt
    assert "REQ-001" in fake_llm.received_prompt
    assert "SCN-001" in fake_llm.received_prompt
    assert "Issue 1" in fake_llm.received_prompt
    assert "Change 1" in fake_llm.received_prompt
    assert "RETRY COUNT:" in fake_llm.received_prompt


def test_test_design_rework_service_rejects_empty_response():
    fake_llm = FakeLLMManager("")

    service = TestDesignReworkService(
        llm_manager=fake_llm
    )

    try:
        service.rework(
            document_name="sample.docx",
            requirement_context="Requirement ID: REQ-001",
            risk_strategy_context="Risk Level: High",
            scenario_context="Scenario ID: SCN-001",
            current_design_context="{}",
            issues=["Issue"],
            required_changes=["Change"],
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "LLM response is empty" in str(exc)


def test_test_design_rework_service_rejects_invalid_json():
    fake_llm = FakeLLMManager(
        "This is not valid JSON."
    )

    service = TestDesignReworkService(
        llm_manager=fake_llm
    )

    try:
        service.rework(
            document_name="sample.docx",
            requirement_context="Requirement ID: REQ-001",
            risk_strategy_context="Risk Level: High",
            scenario_context="Scenario ID: SCN-001",
            current_design_context="{}",
            issues=["Issue"],
            required_changes=["Change"],
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "not valid JSON" in str(exc)


def test_test_design_rework_service_rejects_invalid_schema():
    fake_llm = FakeLLMManager(
        """
        {
          "document_name": "sample.docx",
          "design_summary": "Invalid design"
        }
        """
    )

    service = TestDesignReworkService(
        llm_manager=fake_llm
    )

    try:
        service.rework(
            document_name="sample.docx",
            requirement_context="Requirement ID: REQ-001",
            risk_strategy_context="Risk Level: High",
            scenario_context="Scenario ID: SCN-001",
            current_design_context="{}",
            issues=["Issue"],
            required_changes=["Change"],
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert (
            "does not conform to TestDesignAnalysis schema"
            in str(exc)
        )
