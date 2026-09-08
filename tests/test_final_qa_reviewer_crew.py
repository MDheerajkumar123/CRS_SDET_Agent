
from app.final_review.crew.final_qa_reviewer_crew import (
    FinalQAReviewerCrew,
)


def test_final_qa_reviewer_crew_construction():
    crew_wrapper = FinalQAReviewerCrew(
        document_name="sample.docx",
        requirement_context="REQ-001: Login",
        risk_strategy_context="REQ-001: High risk",
        scenario_context="SCN-001: Valid login",
        test_design_context="TD-001: Login design",
        test_case_context="TC-001: Login test",
        rtm_context="REQ-001: Covered",
    )

    crew = crew_wrapper.get_crew()

    assert crew is not None
    assert len(crew.agents) == 1
    assert len(crew.tasks) == 1
    assert crew.agents[0].role == "Senior SDET Final QA Reviewer"
