
from crewai import Task

from app.rtm.validation.agents.rtm_validation_agent import (
    RTMValidationAgent,
)
from app.rtm.validation.prompts.rtm_validator import (
    build_rtm_validator_prompt,
)


def create_rtm_validation_task(
    document_name: str,
    requirement_context: str,
    scenario_context: str,
    test_design_context: str,
    test_case_context: str,
    rtm_context: str,
):
    agent_wrapper = RTMValidationAgent()

    prompt = build_rtm_validator_prompt(
        document_name=document_name,
        requirement_context=requirement_context,
        scenario_context=scenario_context,
        test_design_context=test_design_context,
        test_case_context=test_case_context,
        rtm_context=rtm_context,
    )

    return Task(
        description=prompt,
        expected_output=(
            "A JSON object containing status, score, issues, "
            "and required_changes."
        ),
        agent=agent_wrapper.agent,
        output_pydantic=__import__(
            "app.rtm.validation.models.review_result",
            fromlist=["RTMReviewResult"],
        ).RTMReviewResult,
    )
