
from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.strategy.models.test_strategy import TestStrategy
from app.strategy.services.risk_strategy_rework_service import (
    RiskStrategyReworkService,
)


class RiskStrategyReworkHandler:
    """
    Adapter between the Final QA rework workflow and the
    Risk Strategy rework workflow.

    This handler is responsible only for RISK_STRATEGY rework.
    """

    EXPECTED_ARTIFACT = "RISK_STRATEGY"
    EXPECTED_ROUTE = "risk_strategy"

    def __init__(self, rework_service=None):
        self.rework_service = (
            rework_service or RiskStrategyReworkService()
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

        risk_strategy_context = current_context.get(
            "risk_strategy_context"
        )

        if risk_strategy_context is None:
            raise ValueError(
                "current_context must contain risk_strategy_context"
            )

        revised_strategy = self.rework_service.rework(
            document_name=request.document_name,
            requirement_context=request.requirement_context,
            current_strategy=risk_strategy_context,
            issues=request.issues,
            required_changes=request.required_changes,
            retry_count=request.retry_count,
        )

        if not isinstance(revised_strategy, TestStrategy):
            raise TypeError(
                "RiskStrategyReworkService must return a "
                "TestStrategy instance"
            )

        return {
            "risk_strategy_context": (
                revised_strategy.model_dump_json(indent=2)
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
                "RiskStrategyReworkHandler requires a "
                "RISK_STRATEGY route"
            )

        for route in matching_routes:
            if route.get("route") != self.EXPECTED_ROUTE:
                raise ValueError(
                    "RISK_STRATEGY must route to risk_strategy"
                )
