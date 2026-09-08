
from types import SimpleNamespace

from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.final_review.services.final_qa_rework_service import (
    FinalQAReworkService,
    FinalQAReworkResult,
)


class FakeLLMManager:
    def generate(self, task_name, prompt):
        assert task_name == "final_reviewer"
        assert "Security coverage is missing." in prompt
        assert "Add appropriate security coverage." in prompt

        return SimpleNamespace(
            content="""
            {
                "document_name": "sample.docx",
                "rework_targets": [
                    {
                        "artifact": "SCENARIOS",
                        "reason": "Security coverage is missing.",
                        "actions": [
                            "Add source-supported security scenarios."
                        ]
                    },
                    {
                        "artifact": "TEST_CASES",
                        "reason": "Security test cases are missing.",
                        "actions": [
                            "Add test cases for approved security scenarios."
                        ]
                    }
                ],
                "overall_rework_summary": "Scenario and test case coverage require rework."
            }
            """
        )


def test_final_qa_rework_service():
    request = FinalQAReworkRequest(
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

    service = FinalQAReworkService(
        llm_manager=FakeLLMManager()
    )

    result = service.rework(request)

    assert isinstance(result, FinalQAReworkResult)
    assert result.document_name == "sample.docx"
    assert len(result.rework_targets) == 2

    assert result.rework_targets[0].artifact == "SCENARIOS"
    assert (
        "Security coverage is missing."
        in result.rework_targets[0].reason
    )

    assert result.rework_targets[1].artifact == "TEST_CASES"

    assert (
        result.overall_rework_summary
        == "Scenario and test case coverage require rework."
    )
