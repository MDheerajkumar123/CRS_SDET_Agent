import json

from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.rtm.validation.models.rework_request import (
    RTMReworkRequest,
)
from app.rtm.validation.services.rtm_rework_service import (
    RTMReworkService,
)


class RTMReworkHandler:
    """
    Adapter between the Final QA rework workflow and the
    existing RTM rework workflow.

    This handler is responsible only for RTM rework.
    """

    EXPECTED_ARTIFACT = "RTM"
    EXPECTED_ROUTE = "rtm_validation"

    def __init__(self, rework_service=None):
        self.rework_service = (
            rework_service or RTMReworkService()
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

        rtm_context = current_context.get(
            "rtm_context"
        )

        if rtm_context is None:
            raise ValueError(
                "current_context must contain rtm_context"
            )

        rtm_request = RTMReworkRequest(
            document_name=request.document_name,
            current_rtm=rtm_context,
            issues=request.issues,
            required_changes=request.required_changes,
            retry_count=request.retry_count,
        )

        revised_rtm = self.rework_service.rework(
            rtm_request
        )

        return {
            "rtm_context": json.dumps(
                revised_rtm.model_dump(),
                indent=2,
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
                "RTMReworkHandler requires an RTM route"
            )

        for route in matching_routes:
            if route.get("route") != self.EXPECTED_ROUTE:
                raise ValueError(
                    "RTM must route to "
                    "rtm_validation"
                )
