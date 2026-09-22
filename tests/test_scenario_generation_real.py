from app.analysis.services.requirement_analyzer import RequirementAnalyzer
from app.llm.manager import LLMManager
from app.scenario.services.test_scenario_service import TestScenarioService
from app.strategy.services.test_strategy_service import TestStrategyService


def test_real_scenario_generation():
    llm_manager = LLMManager()

    analyzer = RequirementAnalyzer(
        llm_manager=llm_manager
    )

    analysis, _ = analyzer.analyze(
        "Sample.docx",
        "Identify the main customer requirements, business rules, validations, dependencies, and error conditions.",
        n_results=5,
    )

    strategy_service = TestStrategyService(
        llm_manager=llm_manager
    )

    strategy = strategy_service.generate_strategy(
        analysis
    )

    scenario_service = TestScenarioService(
        llm_manager=llm_manager
    )

    scenarios = scenario_service.generate_scenarios(
        analysis,
        strategy,
    )

    assert scenarios.document_name == "Sample.docx"
    assert len(scenarios.scenarios) > 0
    assert 0 <= scenarios.overall_scenario_confidence <= 1

    requirement_ids = {
        requirement.requirement_id
        for requirement in analysis.requirements
    }

    for scenario in scenarios.scenarios:
        assert scenario.requirement_id in requirement_ids

    print()
    print("REAL SCENARIO GENERATION TEST: PASS")
    print("Scenarios:", len(scenarios.scenarios))
    print("Confidence:", scenarios.overall_scenario_confidence)