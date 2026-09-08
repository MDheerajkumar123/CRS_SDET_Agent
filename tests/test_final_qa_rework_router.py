
from app.final_review.models.rework_routing import (
    ReworkArtifact,
    ReworkRoutingResult,
    ReworkTarget,
)
from app.final_review.services.final_qa_rework_router import (
    FinalQAReworkRouter,
)


def test_router_maps_test_cases():
    router = FinalQAReworkRouter()

    result = ReworkRoutingResult(
        document_name="sample_crs.docx",
        targets=[
            ReworkTarget(
                artifact=ReworkArtifact.TEST_CASES,
                reason="Negative coverage is incomplete.",
                actions=["Add missing negative scenarios."],
            )
        ],
        routing_summary="Test case rework required.",
    )

    routed = router.route(result)

    assert routed["document_name"] == "sample_crs.docx"
    assert len(routed["routes"]) == 1
    assert routed["routes"][0]["artifact"] == "TEST_CASES"
    assert routed["routes"][0]["route"] == "test_case_validation"
    assert routed["routes"][0]["reason"] == "Negative coverage is incomplete."


def test_router_maps_all_artifacts():
    router = FinalQAReworkRouter()

    targets = [
        ReworkTarget(
            artifact=artifact,
            reason=f"Rework required for {artifact.value}",
        )
        for artifact in ReworkArtifact
    ]

    result = ReworkRoutingResult(
        document_name="sample_crs.docx",
        targets=targets,
        routing_summary="Multiple artifacts require rework.",
    )

    routed = router.route(result)

    assert len(routed["routes"]) == 6

    expected_routes = {
        "REQUIREMENTS": "requirement_validation",
        "RISK_STRATEGY": "risk_strategy",
        "SCENARIOS": "scenario_validation",
        "TEST_DESIGNS": "test_design",
        "TEST_CASES": "test_case_validation",
        "RTM": "rtm_validation",
    }

    for route in routed["routes"]:
        assert expected_routes[route["artifact"]] == route["route"]


def test_router_preserves_actions():
    router = FinalQAReworkRouter()

    result = ReworkRoutingResult(
        document_name="sample_crs.docx",
        targets=[
            ReworkTarget(
                artifact=ReworkArtifact.RTM,
                reason="Coverage calculation requires correction.",
                actions=[
                    "Recalculate coverage",
                    "Verify requirement traceability",
                ],
            )
        ],
        routing_summary="RTM rework required.",
    )

    routed = router.route(result)

    assert routed["routes"][0]["actions"] == [
        "Recalculate coverage",
        "Verify requirement traceability",
    ]


def test_router_rejects_invalid_input():
    router = FinalQAReworkRouter()

    try:
        router.route("invalid")
        assert False, "Expected TypeError"
    except TypeError as exc:
        assert "ReworkRoutingResult" in str(exc)
