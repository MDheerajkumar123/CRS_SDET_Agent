
from types import SimpleNamespace

from app.final_review.models.review_result import (
    FinalQAReviewResult,
    FinalReviewStatus,
)
from app.final_review.services.final_qa_reviewer_service import (
    FinalQAReviewerService,
)


class FakeLLMManager:
    def generate(self, task_name, prompt):
        assert task_name == "final_reviewer"

        assert "REQ-001: Login" in prompt
        assert "SCN-001: Valid login" in prompt
        assert "TD-001: Login design" in prompt
        assert "TC-001: Login test" in prompt
        assert "REQ-001: Covered" in prompt

        return SimpleNamespace(
            content="""
            {
                "status": "PASS",
                "score": 100,
                "issues": [],
                "required_changes": [],
                "review_summary": "QA package is ready for final delivery."
            }
            """
        )


def test_final_qa_reviewer_service():
    service = FinalQAReviewerService(
        llm_manager=FakeLLMManager()
    )

    result = service.review(
        document_name="sample.docx",
        requirement_context="REQ-001: Login",
        risk_strategy_context="REQ-001: High risk",
        scenario_context="SCN-001: Valid login",
        test_design_context="TD-001: Login design",
        test_case_context="TC-001: Login test",
        rtm_context="REQ-001: Covered",
    )

    assert isinstance(result, FinalQAReviewResult)
    assert result.status == FinalReviewStatus.PASS
    assert result.score == 100
    assert result.issues == []
    assert result.required_changes == []
    assert (
        result.review_summary
        == "QA package is ready for final delivery."
    )
