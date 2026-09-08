from app.final_review.models.rework_routing import (
    ReworkArtifact,
)


class FinalQAReworkDispatcher:
    """
    Selects the correct Final QA rework handler based on
    the routed artifact.

    The dispatcher does not execute rework itself.
    """

    def __init__(
        self,
        requirement_handler,
        risk_strategy_handler,
        scenario_handler,
        test_design_handler,
        test_case_handler,
        rtm_handler,
    ):
        self.handlers = {
            ReworkArtifact.REQUIREMENTS.value: requirement_handler,
            ReworkArtifact.RISK_STRATEGY.value: risk_strategy_handler,
            ReworkArtifact.SCENARIOS.value: scenario_handler,
            ReworkArtifact.TEST_DESIGNS.value: test_design_handler,
            ReworkArtifact.TEST_CASES.value: test_case_handler,
            ReworkArtifact.RTM.value: rtm_handler,
        }

    def get_handler(self, artifact: str):
        """
        Return the registered handler for an artifact.
        """

        if not isinstance(artifact, str):
            raise TypeError(
                "artifact must be a string"
            )

        handler = self.handlers.get(artifact)

        if handler is None:
            raise ValueError(
                f"No Final QA rework handler registered "
                f"for artifact: {artifact}"
            )

        return handler

    def get_handler_for_route(self, route: dict):
        """
        Return the handler for a single validated routing entry.
        """

        if not isinstance(route, dict):
            raise TypeError(
                "route must be a dictionary"
            )

        artifact = route.get("artifact")

        if artifact is None:
            raise ValueError(
                "route must contain an artifact"
            )

        expected_route = {
            ReworkArtifact.REQUIREMENTS.value:
                "requirement_validation",
            ReworkArtifact.RISK_STRATEGY.value:
                "risk_strategy",
            ReworkArtifact.SCENARIOS.value:
                "scenario_validation",
            ReworkArtifact.TEST_DESIGNS.value:
                "test_design",
            ReworkArtifact.TEST_CASES.value:
                "test_case_validation",
            ReworkArtifact.RTM.value:
                "rtm_validation",
        }

        actual_route = route.get("route")

        if actual_route is None:
            raise ValueError(
                f"route for {artifact} must contain a route"
            )

        expected = expected_route.get(artifact)

        if expected is None:
            raise ValueError(
                f"No Final QA rework handler registered "
                f"for artifact: {artifact}"
            )

        if actual_route != expected:
            raise ValueError(
                f"{artifact} must route to {expected}"
            )

        return self.get_handler(artifact)
