
from app.analysis.models.requirement import RequirementAnalysis
from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.validation.models.review_result import (
    ReviewResult,
    ReviewStatus,
)
from app.validation.services.rework_service import (
    RequirementReworkService,
)


class RequirementReworkHandler:
    """
    Adapter between the Final QA rework workflow and the
    existing Requirement rework workflow.

    This handler is responsible only for REQUIREMENTS rework.
    """

    EXPECTED_ARTIFACT = "REQUIREMENTS"
    EXPECTED_ROUTE = "requirement_validation"

    def __init__(self, rework_service=None):
        self.rework_service = (
            rework_service or RequirementReworkService()
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

        requirement_context = current_context.get(
            "requirement_context"
        )

        if requirement_context is None:
            raise ValueError(
                "current_context must contain requirement_context"
            )

        analysis = RequirementAnalysis.model_validate_json(
            requirement_context
        )

        review = ReviewResult(
            status=ReviewStatus.REWORK,
            score=0,
            issues=request.issues,
            required_changes=request.required_changes,
        )

        revised_analysis, _ = self.rework_service.rework(
            analysis=analysis,
            review=review,
        )

        if not isinstance(revised_analysis, RequirementAnalysis):
            raise TypeError(
                "RequirementReworkService must return a "
                "RequirementAnalysis instance"
            )

        return {
            "requirement_context": (
                revised_analysis.model_dump_json(indent=2)
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
                "RequirementReworkHandler requires a "
                "REQUIREMENTS route"
            )

        for route in matching_routes:
            if route.get("route") != self.EXPECTED_ROUTE:
                raise ValueError(
                    "REQUIREMENTS must route to "
                    "requirement_validation"
                )
