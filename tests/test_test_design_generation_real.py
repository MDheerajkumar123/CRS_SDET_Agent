from app.analysis.services.requirement_analyzer import RequirementAnalyzer
from app.llm.manager import LLMManager
from app.scenario.services.test_scenario_service import TestScenarioService
from app.strategy.services.test_strategy_service import TestStrategyService
from app.test_design.services.test_design_service import TestDesignService


def test_real_test_design_generation():
    llm_manager = LLMManager()

    analyzer = RequirementAnalyzer(llm_manager=llm_manager)

    analysis, _ = analyzer.analyze(
        "Sample.docx",
        "Identify the main customer requirements, business rules, "
        "validations, dependencies, and error conditions.",
        n_results=5,
    )

    strategy_service = TestStrategyService(
        llm_manager=llm_manager
    )
    strategy = strategy_service.generate_strategy(analysis)

    scenario_service = TestScenarioService(
        llm_manager=llm_manager
    )
    scenarios = scenario_service.generate_scenarios(
        analysis,
        strategy,
    )

    design_service = TestDesignService(
        llm_manager=llm_manager
    )
    designs = design_service.generate_designs(
        analysis,
        strategy,
        scenarios,
    )

    assert designs.document_name == "Sample.docx"
    assert len(designs.test_designs) > 0
    assert 0 <= designs.overall_design_confidence <= 1

    requirement_ids = {
        requirement.requirement_id
        for requirement in analysis.requirements
    }

    scenario_ids = {
        scenario.scenario_id
        for scenario in scenarios.scenarios
    }

    allowed_techniques = {
        "Equivalence Partitioning",
        "Boundary Value Analysis",
        "Decision Table",
        "State Transition",
        "Error Guessing",
        "Pairwise",
        "Use Case",
    }

    for design in designs.test_designs:
        assert design.requirement_id in requirement_ids
        assert design.scenario_id in scenario_ids
        assert design.test_design_technique.value in allowed_techniques

    print()
    print("REAL TEST DESIGN GENERATION TEST: PASS")
    print("Designs:", len(designs.test_designs))
    print("Confidence:", designs.overall_design_confidence)