
from app.final_review.models.review_result import FinalQAReviewResult
from app.final_review.tasks.final_qa_reviewer_task import (
    create_final_qa_reviewer_task,
)


def test_final_qa_reviewer_task_construction():
    task = create_final_qa_reviewer_task(
        document_name="sample.docx",
        requirement_context="REQ-001: Login",
        risk_strategy_context="REQ-001: High risk",
        scenario_context="SCN-001: Valid login",
        test_design_context="TD-001: Login design",
        test_case_context="TC-001: Login test",
        rtm_context="REQ-001: Covered",
    )

    assert task is not None
    assert task.agent is not None
    assert task.output_pydantic == FinalQAReviewResult
    assert "FINAL REVIEW CRITERIA" in task.description
