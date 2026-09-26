from app.analysis.models.requirement import RequirementAnalysis
from app.scenario.models.test_scenario import ScenarioAnalysis
from app.scenario.validation.models.loop_result import (
    ScenarioValidationLoopResult,
)
from app.scenario.validation.models.review_result import (
    ScenarioReviewResult,
    ScenarioReviewStatus,
)
from app.scenario.validation.services.scenario_validator_service import (
    ScenarioValidatorService,
)
from app.scenario.validation.services.scenario_rework_service import (
    ScenarioReworkService,
)
from app.strategy.models.test_strategy import TestStrategy


class ScenarioValidationLoop:
    def __init__(
        self,
        validator=None,
        rework_service=None,
        max_retries: int = 3,
        event_publisher=None,
    ):
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1.")

        self.validator = validator or ScenarioValidatorService()
        self.rework_service = (
            rework_service or ScenarioReworkService()
        )
        self.max_retries = max_retries
        self.event_publisher = event_publisher

    def _emit(self, event_type, **metadata):
        if self.event_publisher:
            self.event_publisher({"event_type": event_type, "stage": "Scenario Validator", "message": "Scenario validation requires rework." if event_type == "REWORK_STARTED" else "Scenario artifact reworked.", "metadata": metadata})

    def run(
        self,
        analysis: RequirementAnalysis,
        strategy: TestStrategy,
        scenarios: ScenarioAnalysis,
        requirement_context: str,
        risk_strategy_context: str,
    ) -> ScenarioValidationLoopResult:

        if not isinstance(analysis, RequirementAnalysis):
            raise TypeError(
                "analysis must be a RequirementAnalysis instance."
            )

        if not isinstance(strategy, TestStrategy):
            raise TypeError(
                "strategy must be a TestStrategy instance."
            )

        if not isinstance(scenarios, ScenarioAnalysis):
            raise TypeError(
                "scenarios must be a ScenarioAnalysis instance."
            )

        current_scenarios = scenarios
        retry_count = 0

        while True:
            review = self.validator.validate(
                analysis=analysis,
                strategy=strategy,
                scenarios=current_scenarios,
            )

            if review.status == ScenarioReviewStatus.PASS:
                return ScenarioValidationLoopResult(
                    final_scenarios=current_scenarios,
                    final_review=review,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=True,
                )

            if retry_count >= self.max_retries:
                return ScenarioValidationLoopResult(
                    final_scenarios=current_scenarios,
                    final_review=review,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=False,
                )

            self._emit("REWORK_STARTED", attempt=retry_count + 1, issues=review.issues, score=getattr(review, "score", None))
            current_scenarios, _ = self.rework_service.rework(
                scenarios=current_scenarios,
                review=review,
                document_name=analysis.document_name,
                requirement_context=requirement_context,
                risk_strategy_context=risk_strategy_context,
                retry_count=retry_count + 1,
            )

            retry_count += 1
            self._emit("REWORK_COMPLETED", attempt=retry_count)
