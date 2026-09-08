
import json

from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.test_case.validation.models.rework_request import (
    TestCaseReworkRequest,
)
from app.test_case.validation.services.test_case_rework_service import (
    TestCaseReworkService,
)


class TestCaseReworkHandler:
    """
    Adapter between the Final QA rework workflow and the
    existing Test Case rework workflow.

    This handler is responsible only for TEST_CASES rework.
    """

    EXPECTED_ARTIFACT = "TEST_CASES"
    EXPECTED_ROUTE = "test_case_validation"

    def __init__(self, rework_service=None):
        self.rework_service = (
            rework_service or TestCaseReworkService()
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

        test_case_context = current_context.get(
            "test_case_context"
        )

        if test_case_context is None:
            raise ValueError(
                "current_context must contain test_case_context"
            )

        test_case_request = TestCaseReworkRequest(
            document_name=request.document_name,
            current_test_cases=test_case_context,
            issues=request.issues,
            required_changes=request.required_changes,
            retry_count=request.retry_count,
        )

        revised_test_cases = self.rework_service.rework(
            test_case_request
        )

        return {
            "test_case_context": json.dumps(
                revised_test_cases.model_dump(),
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
                "TestCaseReworkHandler requires a TEST_CASES route"
            )

        for route in matching_routes:
            if route.get("route") != self.EXPECTED_ROUTE:
                raise ValueError(
                    "TEST_CASES must route to "
                    "test_case_validation"
                )
