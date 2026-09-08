from app.test_case.validation.tasks.test_case_validation_task import (
    TestCaseValidationTask,
)


def test_test_case_validation_task_construction():
    task = TestCaseValidationTask(
        document_name="Sample_CRS.docx",
        requirement_context="Requirement context",
        risk_strategy_context="Risk strategy context",
        scenario_context="Scenario context",
        test_design_context="Test design context",
        test_case_context="Test case context",
    ).create_task()

    assert task is not None
    assert task.agent is not None
    assert task.output_pydantic is not None

    print("Test Test Case Validation Task Construction PASS")
