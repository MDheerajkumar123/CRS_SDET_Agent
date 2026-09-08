
import json
from pathlib import Path

from app.rtm.crew.rtm_crew import RTMCrew
from app.rtm.models.rtm import RTMAnalysis


FIXTURE_PATH = Path(
    "data/test_case_analysis_reworked.json"
)


def test_real_rtm_execution():
    # ---------------------------------------------------------
    # 1. Load approved/reworked test cases
    # ---------------------------------------------------------
    assert FIXTURE_PATH.exists(), (
        f"Fixture not found: {FIXTURE_PATH}"
    )

    test_case_data = json.loads(
        FIXTURE_PATH.read_text(encoding="utf-8")
    )

    # Validate fixture structure before sending it to the LLM.
    test_case_analysis = test_case_data

    assert test_case_analysis["test_cases"], (
        "Test Case fixture contains no test cases."
    )

    test_case_context = json.dumps(
        test_case_analysis,
        indent=2,
    )

    print(
        f"Loaded test cases: "
        f"{len(test_case_analysis['test_cases'])}"
    )

    # ---------------------------------------------------------
    # 2. Controlled upstream contexts
    # ---------------------------------------------------------
    requirement_context = """
REQ-001:
A valid payment must be processed successfully after
gateway confirmation.

REQ-002:
Repeated payment attempts must not create duplicate charges.

REQ-003:
Sensitive payment information must be protected and masked.

REQ-004:
Payment failure must result in an appropriate failure status.

REQ-005:
Payment retry behavior must be handled safely.

REQ-006:
Successful payment status must depend on gateway confirmation.
"""

    scenario_context = """
SCN-001 → REQ-001:
Valid payment success.

SCN-002 → REQ-002:
Duplicate payment prevention.

SCN-003 → REQ-003:
Sensitive payment data protection.

SCN-004 → REQ-004:
Payment failure handling.

SCN-005 → REQ-005:
Payment retry safety.

SCN-006 → REQ-006:
Gateway-confirmed payment success.
"""

    test_design_context = """
TD-001 → SCN-001 → REQ-001:
Positive payment success design.

TD-002 → SCN-002 → REQ-002:
Duplicate payment prevention design.

TD-003 → SCN-003 → REQ-003:
Sensitive data protection design.

TD-004 → SCN-004 → REQ-004:
Payment failure design.

TD-005 → SCN-005 → REQ-005:
Payment retry design.

TD-006 → SCN-006 → REQ-006:
Gateway confirmation design.
"""

    # Risk context is intentionally concise and evidence-based.
    risk_strategy_context = """
REQ-001: Critical risk. Functional and Negative testing required.

REQ-002: Critical risk. Negative and Integration testing required.

REQ-003: Critical risk. Security testing required.

REQ-004: High risk. Negative testing required.

REQ-005: High risk. Negative and Integration testing required.

REQ-006: Critical risk. Functional and Integration testing required.
"""

    # ---------------------------------------------------------
    # 3. Create RTM Crew
    # ---------------------------------------------------------
    rtm_crew = RTMCrew(
        document_name=test_case_analysis["document_name"],
        requirement_context=requirement_context,
        scenario_context=scenario_context,
        test_design_context=test_design_context,
        test_case_context=test_case_context,
    )

    # ---------------------------------------------------------
    # 4. Real CrewAI kickoff
    # ---------------------------------------------------------
    result = rtm_crew.kickoff()

    # ---------------------------------------------------------
    # 5. Validate structured output
    # ---------------------------------------------------------
    assert result is not None

    if hasattr(result, "pydantic") and result.pydantic:
        rtm_analysis = result.pydantic
    else:
        rtm_analysis = RTMAnalysis.model_validate(
            json.loads(result.raw)
        )

    assert isinstance(rtm_analysis, RTMAnalysis)
    assert rtm_analysis.document_name == (
        test_case_analysis["document_name"]
    )

    assert rtm_analysis.total_requirements == 6

    assert len(rtm_analysis.requirement_coverage) == 6

    assert (
        rtm_analysis.covered_requirements
        + rtm_analysis.partially_covered_requirements
        + rtm_analysis.not_covered_requirements
        == rtm_analysis.total_requirements
    )

    assert 0 <= rtm_analysis.overall_coverage_percentage <= 100

    # Ensure the LLM did not invent requirement IDs.
    requirement_ids = {
        item.requirement_id
        for item in rtm_analysis.requirement_coverage
    }

    expected_requirement_ids = {
        "REQ-001",
        "REQ-002",
        "REQ-003",
        "REQ-004",
        "REQ-005",
        "REQ-006",
    }

    assert requirement_ids == expected_requirement_ids

    # ---------------------------------------------------------
    # 6. Print useful result
    # ---------------------------------------------------------
    print(
        f"RTM requirements: "
        f"{rtm_analysis.total_requirements}"
    )

    print(
        f"Covered: "
        f"{rtm_analysis.covered_requirements}"
    )

    print(
        f"Partial: "
        f"{rtm_analysis.partially_covered_requirements}"
    )

    print(
        f"Not covered: "
        f"{rtm_analysis.not_covered_requirements}"
    )

    print(
        f"Overall coverage: "
        f"{rtm_analysis.overall_coverage_percentage}%"
    )

    print(
        "REAL RTM EXECUTION PASS"
    )
