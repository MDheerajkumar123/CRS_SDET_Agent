
from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.test_design.models.test_design import (
    TestDesignAnalysis,
)
from app.test_design.services.test_design_rework_service import (
    TestDesignReworkService,
)


class TestDesignReworkHandler:
    """
    Adapter between the Final QA rework workflow and the
    existing Test Design rework workflow.

    This handler is responsible only for TEST_DESIGNS rework.
    """

    EXPECTED_ARTIFACT = "TEST_DESIGNS"
    EXPECTED_ROUTE = "test_design"

    def __init__(self, rework_service=None):
        self.rework_service = (
            rework_service or TestDesignReworkService()
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

        test_design_context = current_context.get(
            "test_design_context"
        )

        if test_design_context is None:
            raise ValueError(
                "current_context must contain test_design_context"
            )

        revised_designs = self.rework_service.rework(
            document_name=request.document_name,
            requirement_context=request.requirement_context,
            risk_strategy_context=request.risk_strategy_context,
            scenario_context=request.scenario_context,
            current_design_context=test_design_context,
            issues=request.issues,
            required_changes=request.required_changes,
            retry_count=request.retry_count,
        )

        if not isinstance(revised_designs, TestDesignAnalysis):
            raise TypeError(
                "TestDesignReworkService must return a "
                "TestDesignAnalysis instance"
            )

        return {
            "test_design_context": (
                revised_designs.model_dump_json(indent=2)
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
                "TestDesignReworkHandler requires a "
                "TEST_DESIGNS route"
            )

        for route in matching_routes:
            if route.get("route") != self.EXPECTED_ROUTE:
                raise ValueError(
                    "TEST_DESIGNS must route to test_design"
                )
