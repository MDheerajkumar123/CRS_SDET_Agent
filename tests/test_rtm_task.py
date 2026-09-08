
from app.rtm.tasks.rtm_task import create_rtm_task


def test_rtm_task_construction():
    task = create_rtm_task(
        document_name="SmartBank_CRS.docx",
        requirement_context="REQ-001: Valid payment.",
        scenario_context="SCN-001 → REQ-001.",
        test_design_context="TD-001 → SCN-001.",
        test_case_context="TC-001 → TD-001.",
    )

    assert task is not None
    assert task.agent is not None
    assert task.output_pydantic == __import__(
        "app.rtm.models.rtm",
        fromlist=["RTMAnalysis"],
    ).RTMAnalysis

    assert "REQ-001" in task.description
    assert "SCN-001" in task.description
    assert "TD-001" in task.description
    assert "TC-001" in task.description

    print("RTM task construction PASS")
