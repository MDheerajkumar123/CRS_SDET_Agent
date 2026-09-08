
import json
from pathlib import Path

from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.validation.models.rework_request import (
    TestCaseReworkRequest,
)
from app.test_case.validation.services.test_case_rework_service import (
    TestCaseReworkService,
)


FIXTURE_PATH = Path("data/test_case_analysis_latest.json")
REWORKED_FIXTURE_PATH = Path(
    "data/test_case_analysis_reworked.json"
)


def test_real_test_case_rework_integration():
    # ---------------------------------------------------------
    # 1. Load previously generated TestCaseAnalysis
    # ---------------------------------------------------------
    assert FIXTURE_PATH.exists(), (
        f"Test Case fixture not found: {FIXTURE_PATH}"
    )

    fixture_data = json.loads(
        FIXTURE_PATH.read_text(encoding="utf-8")
    )

    test_case_analysis = TestCaseAnalysis.model_validate(
        fixture_data
    )

    assert len(test_case_analysis.test_cases) > 0

    print(
        f"Loaded test cases: "
        f"{len(test_case_analysis.test_cases)}"
    )

    # ---------------------------------------------------------
    # 2. Create rework request using real validator findings
    # ---------------------------------------------------------
    request = TestCaseReworkRequest(
        document_name=test_case_analysis.document_name,
        current_test_cases=(
            test_case_analysis.model_dump_json(indent=2)
        ),
        issues=[
            "Multiple test cases have incorrect test_type "
            "classifications that do not align with their "
            "scenario objectives.",
            "TC-006 Functional classification is inappropriate "
            "for duplicate payment prevention and should be "
            "Negative.",
            "TC-007 Functional classification is inappropriate "
            "for payment retry safety and should be Negative.",
            "TC-009 should use a more appropriate test type "
            "for gateway interaction and state transitions.",
        ],
        required_changes=[
            "Change TC-006 test_type from Functional to Negative.",
            "Change TC-007 test_type from Functional to Negative.",
            "Review TC-003 test_type and align it with negative "
            "behavior testing.",
            "Consider changing TC-009 test_type to Integration.",
            "Preserve complete Requirement → Scenario → "
            "Test Design → Test Case traceability.",
        ],
        retry_count=1,
    )

    # ---------------------------------------------------------
    # 3. Real Test Case Rework
    # ---------------------------------------------------------
    rework_service = TestCaseReworkService()

    revised_analysis = rework_service.rework(request)

    assert isinstance(
        revised_analysis,
        TestCaseAnalysis,
    )

    assert len(revised_analysis.test_cases) > 0

    print(
        f"Reworked test cases: "
        f"{len(revised_analysis.test_cases)}"
    )

    print(
        f"Reworked confidence: "
        f"{revised_analysis.overall_test_case_confidence}"
    )

    # ---------------------------------------------------------
    # 4. Save reworked TestCaseAnalysis
    # ---------------------------------------------------------
    REWORKED_FIXTURE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REWORKED_FIXTURE_PATH.write_text(
        revised_analysis.model_dump_json(indent=2),
        encoding="utf-8",
    )

    print(
        f"Saved reworked TestCaseAnalysis fixture: "
        f"{REWORKED_FIXTURE_PATH}"
    )

    # ---------------------------------------------------------
    # 5. Basic traceability validation
    # ---------------------------------------------------------
    for test_case in revised_analysis.test_cases:
        assert test_case.test_case_id
        assert test_case.design_id
        assert test_case.scenario_id
        assert test_case.requirement_id
        assert test_case.source_design

    print(
        "REAL TEST CASE REWORK INTEGRATION PASS"
    )
