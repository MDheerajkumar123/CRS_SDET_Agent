
from app.rtm.validation.tasks.rtm_validation_task import (
    create_rtm_validation_task,
)


def test_rtm_validation_task_construction():
    task = create_rtm_validation_task(
        document_name="sample.docx",
        requirement_context="REQ-001: Login requirement",
        scenario_context="SCN-001: Valid login",
        test_design_context="TD-001: Login design",
        test_case_context="TC-001: Valid login test",
        rtm_context="REQ-001 is fully covered.",
    )

    assert task is not None
    assert task.agent is not None
    assert task.output_pydantic is not None
    assert "RTM" in task.description
