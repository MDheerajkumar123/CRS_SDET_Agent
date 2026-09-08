from app.analysis.services.requirement_analyzer import RequirementAnalyzer
from app.llm.manager import LLMManager
from app.strategy.services.test_strategy_service import TestStrategyService


def test_real_risk_strategy_generation():
    llm_manager = LLMManager()

    analyzer = RequirementAnalyzer(
        llm_manager=llm_manager
    )

    analysis, _ = analyzer.analyze(
        "Sample.docx",
        "Identify the main customer requirements, business rules, validations, dependencies, and error conditions.",
        n_results=5,
    )

    service = TestStrategyService(
        llm_manager=llm_manager
    )

    strategy = service.generate_strategy(
        analysis
    )

    assert strategy.document_name == "Sample.docx"
    assert len(strategy.requirement_risks) > 0
    assert len(strategy.prioritized_requirements) > 0
    assert 0 <= strategy.overall_strategy_confidence <= 1

    print()
    print("REAL RISK AND TEST STRATEGY TEST: PASS")
    print("Provider configured: OpenRouter")
    print("Model configured: Nemotron free")
    print("Document:", strategy.document_name)
    print("Risks:", len(strategy.requirement_risks))
    print("Prioritized requirements:", len(strategy.prioritized_requirements))
    print("Overall risk:", strategy.overall_risk_level)
    print("Confidence:", strategy.overall_strategy_confidence)
