
import json
from pathlib import Path

from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.validation.services.test_case_validator_service import (
    TestCaseValidatorService,
)


FIXTURE_PATH = Path(
    "data/test_case_analysis_reworked.json"
)


def test_real_reworked_test_case_validation():
    # ---------------------------------------------------------
    # 1. Load reworked TestCaseAnalysis
    # ---------------------------------------------------------
    assert FIXTURE_PATH.exists(), (
        f"Reworked Test Case fixture not found: "
        f"{FIXTURE_PATH}"
    )

    fixture_data = json.loads(
        FIXTURE_PATH.read_text(encoding="utf-8")
    )

    test_case_analysis = TestCaseAnalysis.model_validate(
        fixture_data
    )

    assert len(test_case_analysis.test_cases) > 0

    print(
        f"Loaded reworked test cases: "
        f"{len(test_case_analysis.test_cases)}"
    )

    print(
        f"Reworked confidence: "
        f"{test_case_analysis.overall_test_case_confidence}"
    )

    # ---------------------------------------------------------
    # 2. Build validation contexts
    # ---------------------------------------------------------
    requirement_context = """
REQ-001 / BR-001:
A valid payment must be processed successfully after
gateway confirmation.

BR-003:
Repeated payment attempts must not create duplicate charges.

BR-007:
Sensitive payment information must be protected and masked.
"""

    risk_strategy_context = """
BR-001: Critical risk.
Recommended testing: Functional, Negative.

BR-003: Critical risk.
Recommended testing: Negative, Integration.

BR-007: Critical risk.
Recommended testing: Security.
"""

    scenario_context = """
SCN-001 → BR-001:
Valid UPI Payment Success.

SCN-003 → BR-003:
Duplicate Charge Prevention.

SCN-005 → BR-007:
Sensitive Data Protection.

SCN-006 → FR-PAY-010:
Duplicate Payment Prevention.

SCN-007 → FR-PAY-009:
Payment Retry Safety.

SCN-009 → PS-003:
Successful Status Requires Gateway Confirmation.
"""

    test_design_context = """
TD-001 → SCN-001 → BR-001:
Valid UPI Payment Success.

TD-003 → SCN-003 → BR-003:
Duplicate Charge Prevention.

TD-005 → SCN-005 → BR-007:
Sensitive Data Protection.

TD-006 → SCN-006 → FR-PAY-010:
Duplicate Payment Prevention.

TD-007 → SCN-007 → FR-PAY-009:
Payment Retry Safety.

TD-009 → SCN-009 → PS-003:
Successful Status Requires Gateway Confirmation.
"""

    # ---------------------------------------------------------
    # 3. Real validation of reworked test cases
    # ---------------------------------------------------------
    validator_service = TestCaseValidatorService()

    review = validator_service.validate(
        document_name=test_case_analysis.document_name,
        requirement_context=requirement_context,
        risk_strategy_context=risk_strategy_context,
        scenario_context=scenario_context,
        test_design_context=test_design_context,
        test_case_analysis=test_case_analysis,
    )

    # ---------------------------------------------------------
    # 4. Validate reviewer response
    # ---------------------------------------------------------
    assert review is not None
    assert review.status.value in {"PASS", "REWORK"}
    assert 0 <= review.score <= 100

    print(
        f"Second validation status: "
        f"{review.status.value}"
    )

    print(
        f"Second validation score: "
        f"{review.score}"
    )

    print(
        f"Remaining issues: "
        f"{len(review.issues)}"
    )

    print(
        f"Remaining required changes: "
        f"{len(review.required_changes)}"
    )

    if review.issues:
        print("\nRemaining validation issues:")

        for issue in review.issues:
            print(f"- {issue}")

    if review.required_changes:
        print("\nRemaining required changes:")

        for change in review.required_changes:
            print(f"- {change}")

    print(
        "\nREAL REWORKED TEST CASE VALIDATION PASS"
    )
