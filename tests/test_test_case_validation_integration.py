
from pathlib import Path

from app.analysis.models.requirement import RequirementAnalysis
from app.crew.crs_analyzer_crew import CRSAnalyzerCrew
from app.strategy.crew.risk_strategy_crew import RiskStrategyCrew
from app.scenario.crew.test_scenario_crew import TestScenarioCrew
from app.test_design.crew.test_design_crew import TestDesignCrew
from app.test_case.crew.test_case_crew import TestCaseCrew

from app.test_case.validation.services.test_case_validator_service import (
    TestCaseValidatorService,
)


DOCUMENT_NAME = "SmartBank_BRD_ERD_AI_Practice_New.docx"


def test_real_test_case_validation_integration():
    # ---------------------------------------------------------
    # 1. CRS Analyzer
    # ---------------------------------------------------------
    analyzer_crew = CRSAnalyzerCrew(
        document_name=DOCUMENT_NAME,
        query=(
            "Identify all testable requirements, business rules, "
            "errors, dependencies, and QA-relevant requirements."
        ),
        n_results=5,
    )

    analyzer_result = analyzer_crew.kickoff()
    analysis = analyzer_result.pydantic

    assert isinstance(analysis, RequirementAnalysis)
    assert len(analysis.requirements) > 0

    print(
        f"Requirements generated: "
        f"{len(analysis.requirements)}"
    )

    # ---------------------------------------------------------
    # 2. Risk & Test Strategy
    # ---------------------------------------------------------
    requirement_context = analysis.model_dump_json(indent=2)

    risk_crew = RiskStrategyCrew(
        document_name=DOCUMENT_NAME,
        requirement_context=requirement_context,
    ).build()

    risk_result = risk_crew.kickoff()
    strategy = risk_result.pydantic

    assert strategy is not None
    assert len(strategy.requirement_risks) > 0

    risk_strategy_context = strategy.model_dump_json(indent=2)

    print(
        f"Risk entries generated: "
        f"{len(strategy.requirement_risks)}"
    )

    # ---------------------------------------------------------
    # 3. Test Scenario
    # ---------------------------------------------------------
    scenario_crew = TestScenarioCrew(
        document_name=DOCUMENT_NAME,
        requirement_context=requirement_context,
        risk_strategy_context=risk_strategy_context,
    ).build()

    scenario_result = scenario_crew.kickoff()
    scenario_analysis = scenario_result.pydantic

    assert scenario_analysis is not None
    assert len(scenario_analysis.scenarios) > 0

    scenario_context = scenario_analysis.model_dump_json(indent=2)

    print(
        f"Scenarios generated: "
        f"{len(scenario_analysis.scenarios)}"
    )

    # ---------------------------------------------------------
    # 4. Test Design
    # ---------------------------------------------------------
    design_crew = TestDesignCrew(
        document_name=DOCUMENT_NAME,
        requirement_context=requirement_context,
        risk_strategy_context=risk_strategy_context,
        scenario_context=scenario_context,
    ).build()

    design_result = design_crew.kickoff()
    design_analysis = design_result.pydantic

    assert design_analysis is not None
    assert len(design_analysis.test_designs) > 0

    test_design_context = design_analysis.model_dump_json(indent=2)

    print(
        f"Test designs generated: "
        f"{len(design_analysis.test_designs)}"
    )

    # ---------------------------------------------------------
    # 5. Test Case
    # ---------------------------------------------------------
    test_case_crew = TestCaseCrew(
        document_name=DOCUMENT_NAME,
        requirement_context=requirement_context,
        risk_strategy_context=risk_strategy_context,
        scenario_context=scenario_context,
        test_design_context=test_design_context,
    ).build()

    test_case_result = test_case_crew.kickoff()
    test_case_analysis = test_case_result.pydantic

    assert test_case_analysis is not None
    assert len(test_case_analysis.test_cases) > 0

    test_case_context = test_case_analysis.model_dump_json(
        indent=2
    )

    print(
        f"Test cases generated: "
        f"{len(test_case_analysis.test_cases)}"
    )

    # ---------------------------------------------------------
    # Save generated TestCaseAnalysis as reusable fixture
    # ---------------------------------------------------------
    data_directory = Path("data")
    data_directory.mkdir(exist_ok=True)

    fixture_path = (
        data_directory / "test_case_analysis_latest.json"
    )

    fixture_path.write_text(
        test_case_context,
        encoding="utf-8",
    )

    print(
        f"Saved TestCaseAnalysis fixture: "
        f"{fixture_path}"
    )

    # ---------------------------------------------------------
    # 6. Real Test Case Validation
    # ---------------------------------------------------------
    validator_service = TestCaseValidatorService()

    review = validator_service.validate(
        document_name=DOCUMENT_NAME,
        requirement_context=requirement_context,
        risk_strategy_context=risk_strategy_context,
        scenario_context=scenario_context,
        test_design_context=test_design_context,
        test_case_analysis=test_case_analysis,
    )

    assert review is not None
    assert review.status.value in {"PASS", "REWORK"}
    assert 0 <= review.score <= 100

    print(
        f"Validation status: "
        f"{review.status.value}"
    )

    print(
        f"Validation score: "
        f"{review.score}"
    )

    print(
        f"Issues found: "
        f"{len(review.issues)}"
    )

    print(
        f"Required changes: "
        f"{len(review.required_changes)}"
    )

    if review.issues:
        print("\nValidation issues:")

        for issue in review.issues:
            print(f"- {issue}")

    if review.required_changes:
        print("\nRequired changes:")

        for change in review.required_changes:
            print(f"- {change}")

    print(
        "\nREAL TEST CASE VALIDATION KICKOFF PASS"
    )
