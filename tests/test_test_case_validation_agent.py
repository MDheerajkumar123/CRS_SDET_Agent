from app.test_case.validation.agents.test_case_validation_agent import (
    TestCaseValidationAgent,
)


def test_test_case_validation_agent_construction():
    agent = TestCaseValidationAgent().get_agent()

    assert agent is not None
    assert agent.role == "Senior SDET Test Case Validation Reviewer"
    assert agent.allow_delegation is False
    assert agent.max_iter == 5

    print("Test Test Case Validation Agent Construction PASS")
