from app.test_case.validation.crew.test_case_validation_crew import (
    TestCaseValidationCrew,
)


def test_test_case_validation_crew_construction():
    crew = TestCaseValidationCrew(
        document_name="Sample_CRS.docx",
        requirement_context="Requirement context",
        risk_strategy_context="Risk strategy context",
        scenario_context="Scenario context",
        test_design_context="Test design context",
        test_case_context="Test case context",
    ).build()

    assert crew is not None
    assert len(crew.agents) == 1
    assert len(crew.tasks) == 1

    print("Test Test Case Validation Crew Construction PASS")
