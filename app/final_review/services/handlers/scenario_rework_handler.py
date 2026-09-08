from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.scenario.models.test_scenario import ScenarioAnalysis
from app.scenario.validation.models.review_result import (
    ScenarioReviewResult,
)
from app.scenario.validation.services.scenario_rework_service import (
    ScenarioReworkService,
)


class ScenarioReworkHandler:
    """
    Adapter between the Final QA rework workflow and the
    existing Scenario rework workflow.

    This handler is responsible only for SCENARIOS rework.
    """

    EXPECTED_ARTIFACT = "SCENARIOS"
    EXPECTED_ROUTE = "scenario_validation"

    def __init__(self, rework_service=None):
        self.rework_service = (
            rework_service or ScenarioReworkService()
        )

    def handle(
        self,
        request: FinalQAReworkRequest,
        rework_result,
        routing_result,
        current_context: dict,
    ) -> dict:

        if not isinstance(request, FinalQAReworkRequest):
            raise TypeError(
                "request must be a FinalQAReworkRequest instance"
            )

        if not isinstance(current_context, dict):
            raise TypeError(
                "current_context must be a dictionary"
            )

        self._validate_route(routing_result)

        scenario_context = current_context.get(
            "scenario_context"
        )

        if scenario_context is None:
            raise ValueError(
                "current_context must contain scenario_context"
            )

        scenarios = ScenarioAnalysis.model_validate_json(
            scenario_context
        )

        review = ScenarioReviewResult(
            status="REWORK",
            score=0,
            issues=request.issues,
            required_changes=request.required_changes,
            review_summary="Final QA rework request.",
        )

        revised_scenarios, _ = self.rework_service.rework(
            scenarios=scenarios,
            review=review,
            document_name=request.document_name,
            requirement_context=request.requirement_context,
            risk_strategy_context=request.risk_strategy_context,
        )

        return {
            "scenario_context": revised_scenarios.model_dump_json(
                indent=2
            )
        }

    def _validate_route(self, routing_result: dict) -> None:
        if not isinstance(routing_result, dict):
            raise TypeError(
                "routing_result must be a dictionary"
            )

        routes = routing_result.get("routes")

        if not isinstance(routes, list):
            raise ValueError(
                "routing_result must contain a routes list"
            )

        matching_routes = [
            route
            for route in routes
            if isinstance(route, dict)
            and route.get("artifact") == self.EXPECTED_ARTIFACT
        ]

        if not matching_routes:
            raise ValueError(
                "ScenarioReworkHandler requires a SCENARIOS route"
            )

        for route in matching_routes:
            if route.get("route") != self.EXPECTED_ROUTE:
                raise ValueError(
                    "SCENARIOS must route to scenario_validation"
                )
