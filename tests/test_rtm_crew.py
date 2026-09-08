
from app.rtm.crew.rtm_crew import RTMCrew


def test_rtm_crew_construction():
    rtm_crew = RTMCrew(
        document_name="SmartBank_CRS.docx",
        requirement_context="REQ-001: Valid payment.",
        scenario_context="SCN-001 → REQ-001.",
        test_design_context="TD-001 → SCN-001.",
        test_case_context="TC-001 → TD-001.",
    )

    crew = rtm_crew.get_crew()

    assert crew is not None
    assert len(crew.agents) == 1
    assert len(crew.tasks) == 1
    assert crew.tasks[0].agent == crew.agents[0]

    print("RTM crew construction PASS")
