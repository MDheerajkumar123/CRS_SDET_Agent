from unittest.mock import Mock

from app.analysis.models.requirement import RequirementAnalysis
from app.scenario.models.test_scenario import ScenarioAnalysis
from app.scenario.validation.models.review_result import (
    ScenarioReviewResult,
    ScenarioReviewStatus,
)
from app.scenario.validation.services.scenario_validation_loop import (
    ScenarioValidationLoop,
)
from app.strategy.models.test_strategy import TestStrategy


def test_scenario_validation_loop_passes_retry_count_to_rework():
    analysis = Mock(spec=RequirementAnalysis)
    analysis.document_name = "Sample.docx"

    strategy = Mock(spec=TestStrategy)
    scenarios = Mock(spec=ScenarioAnalysis)

    review = ScenarioReviewResult(
        status=ScenarioReviewStatus.REWORK,
        score=70,
        issues=["Scenario issue"],
        required_changes=["Fix scenario"],
    )

    final_review = ScenarioReviewResult(
        status=ScenarioReviewStatus.PASS,
        score=100,
        issues=[],
        required_changes=[],
    )

    validator = Mock()
    validator.validate.side_effect = [
        review,
        final_review,
    ]

    rework_service = Mock()
    rework_service.rework.return_value = (scenarios, Mock())

    loop = ScenarioValidationLoop(
        validator=validator,
        rework_service=rework_service,
        max_retries=3,
    )

    result = loop.run(
        analysis=analysis,
        strategy=strategy,
        scenarios=scenarios,
        requirement_context="Requirement context",
        risk_strategy_context="Risk strategy context",
    )

    assert result.passed is True
    assert result.retry_count == 1

    rework_service.rework.assert_called_once()

    call_kwargs = rework_service.rework.call_args.kwargs

    assert call_kwargs["retry_count"] == 1