
from crewai import Task

from app.final_review.agents.final_qa_reviewer_agent import (
    FinalQAReviewerAgent,
)
from app.final_review.models.review_result import FinalQAReviewResult
from app.final_review.prompts.final_qa_reviewer import (
    build_final_qa_reviewer_prompt,
)


def create_final_qa_reviewer_task(
    document_name: str,
    requirement_context: str,
    risk_strategy_context: str,
    scenario_context: str,
    test_design_context: str,
    test_case_context: str,
    rtm_context: str,
):
    agent_wrapper = FinalQAReviewerAgent()

    prompt = build_final_qa_reviewer_prompt(
        document_name=document_name,
        requirement_context=requirement_context,
        risk_strategy_context=risk_strategy_context,
        scenario_context=scenario_context,
        test_design_context=test_design_context,
        test_case_context=test_case_context,
        rtm_context=rtm_context,
    )

    return Task(
        description=prompt,
        expected_output=(
            "A JSON object containing status, score, issues, "
            "required_changes, and review_summary."
        ),
        agent=agent_wrapper.agent,
        output_pydantic=FinalQAReviewResult,
    )
