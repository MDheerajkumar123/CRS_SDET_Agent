
from app.rtm.validation.crew.rtm_validation_crew import (
    RTMValidationCrew,
)


def test_rtm_validation_crew_construction():
    crew_wrapper = RTMValidationCrew(
        document_name="sample.docx",
        requirement_context="REQ-001: Login requirement",
        scenario_context="SCN-001: Valid login",
        test_design_context="TD-001: Login design",
        test_case_context="TC-001: Valid login test",
        rtm_context="REQ-001 is fully covered.",
    )

    crew = crew_wrapper.get_crew()

    assert crew is not None
    assert len(crew.agents) == 1
    assert len(crew.tasks) == 1
    assert crew.agents[0].role == "Senior SDET RTM Validation Reviewer"
