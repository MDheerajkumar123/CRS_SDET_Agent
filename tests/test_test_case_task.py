from app.test_case.tasks.test_case_task import TestCaseTask as CaseTask


def test_test_case_task_uses_the_shared_generation_prompt():
    task = CaseTask(
        document_name="Sample_CRS.docx",
        requirement_context="Requirement context",
        risk_strategy_context="Risk strategy context",
        scenario_context="Scenario context",
        test_design_context="Test design context",
    ).create_task()

    assert "PAIRWISE DESIGNS" in task.description
    assert "TOOLS AND PLATFORM MECHANISMS" in task.description
    assert "UNDERSPECIFIED SECURITY OR OPERATIONS CONTROLS" in task.description
