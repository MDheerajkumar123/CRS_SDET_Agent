
from app.strategy.models.test_strategy import TestStrategy
from app.strategy.services.risk_strategy_rework_service import (
    RiskStrategyReworkService,
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


def valid_strategy_json():
    return """
    {
      "document_name": "sample.docx",
      "strategy_summary": "Reworked risk-based testing strategy.",
      "requirement_risks": [
        {
          "requirement_id": "REQ-001",
          "risk_level": "High",
          "risk_score": 70,
          "risk_reason": "High business impact requirement.",
          "impacted_areas": ["Data integrity"],
          "recommended_test_types": ["Functional", "Negative"]
        }
      ],
      "prioritized_requirements": ["REQ-001"],
      "overall_risk_level": "High",
      "overall_strategy_confidence": 0.9
    }
    """


def test_risk_strategy_rework_service_returns_test_strategy():
    fake_llm = FakeLLMManager(valid_strategy_json())

    service = RiskStrategyReworkService(
        llm_manager=fake_llm
    )

    result = service.rework(
        document_name="sample.docx",
        requirement_context="Requirement ID: REQ-001",
        current_strategy='{"strategy_summary": "Current strategy"}',
        issues=["Risk classification needs correction."],
        required_changes=["Align risk level with risk score."],
        retry_count=1,
    )

    assert isinstance(result, TestStrategy)
    assert result.document_name == "sample.docx"
    assert result.overall_risk_level.value == "High"
    assert result.overall_strategy_confidence == 0.9


def test_risk_strategy_rework_service_uses_correct_llm_task():
    fake_llm = FakeLLMManager(valid_strategy_json())

    service = RiskStrategyReworkService(
        llm_manager=fake_llm
    )

    service.rework(
        document_name="sample.docx",
        requirement_context="Requirement ID: REQ-001",
        current_strategy='{"strategy_summary": "Current strategy"}',
        issues=["Issue 1"],
        required_changes=["Change 1"],
        retry_count=2,
    )

    assert fake_llm.received_task_name == "risk_strategy"
    assert fake_llm.received_prompt is not None
    assert "sample.docx" in fake_llm.received_prompt
    assert "REQ-001" in fake_llm.received_prompt
    assert "Issue 1" in fake_llm.received_prompt
    assert "Change 1" in fake_llm.received_prompt
    assert "RETRY COUNT:" in fake_llm.received_prompt


def test_risk_strategy_rework_service_rejects_empty_response():
    fake_llm = FakeLLMManager("")

    service = RiskStrategyReworkService(
        llm_manager=fake_llm
    )

    try:
        service.rework(
            document_name="sample.docx",
            requirement_context="Requirement ID: REQ-001",
            current_strategy="{}",
            issues=["Issue"],
            required_changes=["Change"],
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "LLM response is empty" in str(exc)


def test_risk_strategy_rework_service_rejects_invalid_json():
    fake_llm = FakeLLMManager(
        "This is not valid JSON."
    )

    service = RiskStrategyReworkService(
        llm_manager=fake_llm
    )

    try:
        service.rework(
            document_name="sample.docx",
            requirement_context="Requirement ID: REQ-001",
            current_strategy="{}",
            issues=["Issue"],
            required_changes=["Change"],
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "not valid JSON" in str(exc)


def test_risk_strategy_rework_service_rejects_invalid_schema():
    fake_llm = FakeLLMManager(
        """
        {
          "document_name": "sample.docx",
          "strategy_summary": "Invalid strategy"
        }
        """
    )

    service = RiskStrategyReworkService(
        llm_manager=fake_llm
    )

    try:
        service.rework(
            document_name="sample.docx",
            requirement_context="Requirement ID: REQ-001",
            current_strategy="{}",
            issues=["Issue"],
            required_changes=["Change"],
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "does not conform to TestStrategy schema" in str(exc)
