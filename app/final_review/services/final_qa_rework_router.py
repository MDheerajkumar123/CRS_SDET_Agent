
from app.final_review.models.rework_routing import (
    ReworkArtifact,
    ReworkRoutingResult,
)


class FinalQAReworkRouter:
    """
    Converts Final QA rework targets into deterministic routing decisions.

    This layer does not execute agents. It only determines which
    upstream workflow should handle each rework target.
    """

    ROUTE_MAP = {
        ReworkArtifact.REQUIREMENTS: "requirement_validation",
        ReworkArtifact.RISK_STRATEGY: "risk_strategy",
        ReworkArtifact.SCENARIOS: "scenario_validation",
        ReworkArtifact.TEST_DESIGNS: "test_design",
        ReworkArtifact.TEST_CASES: "test_case_validation",
        ReworkArtifact.RTM: "rtm_validation",
    }

    def route(self, routing_result: ReworkRoutingResult) -> dict[str, list[dict]]:
        if not isinstance(routing_result, ReworkRoutingResult):
            raise TypeError(
                "routing_result must be a ReworkRoutingResult"
            )

        routes: list[dict] = []

        for target in routing_result.targets:
            routes.append(
                {
                    "artifact": target.artifact.value,
                    "route": self.ROUTE_MAP[target.artifact],
                    "reason": target.reason,
                    "actions": target.actions,
                }
            )

        return {
            "document_name": routing_result.document_name,
            "routes": routes,
        }
