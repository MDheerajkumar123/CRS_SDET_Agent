
from crewai import Task

from app.rtm.agents.rtm_agent import RTMAgent
from app.rtm.models.rtm import RTMAnalysis
from app.rtm.prompts.rtm import build_rtm_prompt


def create_rtm_task(
    document_name: str,
    requirement_context: str,
    scenario_context: str,
    test_design_context: str,
    test_case_context: str,
) -> Task:
    rtm_agent = RTMAgent()

    prompt = build_rtm_prompt(
        document_name=document_name,
        requirement_context=requirement_context,
        scenario_context=scenario_context,
        test_design_context=test_design_context,
        test_case_context=test_case_context,
    )

    return Task(
        description=prompt,
        expected_output=(
            "A valid RTMAnalysis JSON structure containing every "
            "requirement and its evidence-based coverage status."
        ),
        agent=rtm_agent.get_agent(),
        output_pydantic=RTMAnalysis,
    )
