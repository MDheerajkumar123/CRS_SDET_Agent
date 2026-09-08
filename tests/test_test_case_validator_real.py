from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.validation.services.test_case_validator_service import (
    TestCaseValidatorService,
)


def test_real_test_case_validator():
    test_case_analysis = TestCaseAnalysis(
        document_name="CRS Validator Smoke Test",
        test_case_summary="One minimal test case for validator verification",
        test_cases=[],
        overall_test_case_confidence=0.9,
    )

    service = TestCaseValidatorService()

    result = service.validate(
        document_name="CRS Validator Smoke Test",
        requirement_context="REQ-001: User must be able to log in with valid credentials.",
        risk_strategy_context="REQ-001 risk: Medium. Recommended testing: Functional, Negative.",
        scenario_context="SCN-001: Verify successful login with valid credentials.",
        test_design_context="TD-001: Positive functional design for successful login.",
        test_case_analysis=test_case_analysis,
    )

    print("Validator status:", result.status)
    print("Validator score:", result.score)
    print("Validator issues:", result.issues)
    print("Validator required changes:", result.required_changes)

    assert result.status.value in {"PASS", "REWORK"}
    assert 0 <= result.score <= 100

    print("REAL TEST CASE VALIDATOR PASS")
