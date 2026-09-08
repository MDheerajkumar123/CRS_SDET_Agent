
from app.final_review.models.rework_routing import (
    ReworkArtifact,
    ReworkRoutingResult,
    ReworkTarget,
)


def test_rework_routing_result_with_test_cases():
    result = ReworkRoutingResult(
        document_name="sample_crs.docx",
        targets=[
            ReworkTarget(
                artifact=ReworkArtifact.TEST_CASES,
                reason="Test cases do not adequately cover high-risk scenarios.",
                actions=[
                    "Add missing negative coverage",
                    "Review test type classification",
                ],
            )
        ],
        routing_summary="Rework required in test cases.",
    )

    assert result.document_name == "sample_crs.docx"
    assert len(result.targets) == 1
    assert result.targets[0].artifact == ReworkArtifact.TEST_CASES


def test_rework_routing_supports_multiple_artifacts():
    result = ReworkRoutingResult(
        document_name="sample_crs.docx",
        targets=[
            ReworkTarget(
                artifact=ReworkArtifact.SCENARIOS,
                reason="Scenario coverage is incomplete.",
            ),
            ReworkTarget(
                artifact=ReworkArtifact.RTM,
                reason="RTM coverage requires correction.",
            ),
        ],
        routing_summary="Scenario and RTM rework required.",
    )

    assert len(result.targets) == 2
    assert result.targets[0].artifact == ReworkArtifact.SCENARIOS
    assert result.targets[1].artifact == ReworkArtifact.RTM


def test_all_rework_artifacts_are_supported():
    assert set(ReworkArtifact) == {
        ReworkArtifact.REQUIREMENTS,
        ReworkArtifact.RISK_STRATEGY,
        ReworkArtifact.SCENARIOS,
        ReworkArtifact.TEST_DESIGNS,
        ReworkArtifact.TEST_CASES,
        ReworkArtifact.RTM,
    }
