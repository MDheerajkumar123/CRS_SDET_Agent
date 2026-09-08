
from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.final_review.services.handlers.risk_strategy_rework_handler import (
    RiskStrategyReworkHandler,
)
from app.strategy.models.test_strategy import (
    RiskLevel,
    TestStrategy,
)


class FakeRiskStrategyReworkService:
    def __init__(self):
        self.received_args = None

    def rework(
        self,
        document_name,
        requirement_context,
        current_strategy,
        issues,
        required_changes,
        retry_count,
    ):
        self.received_args = {
            "document_name": document_name,
            "requirement_context": requirement_context,
            "current_strategy": current_strategy,
            "issues": issues,
            "required_changes": required_changes,
            "retry_count": retry_count,
        }

        return TestStrategy(
            document_name=document_name,
            strategy_summary="Reworked strategy",
            requirement_risks=[],
            prioritized_requirements=[],
            overall_risk_level=RiskLevel.HIGH,
            overall_strategy_confidence=0.9,
        )


def build_request():
    return FinalQAReworkRequest(
        document_name="sample.docx",
        requirement_context='{"requirements": []}',
        risk_strategy_context='{"strategy_summary": "Current strategy"}',
        scenario_context='{"scenarios": []}',
        test_design_context='{"test_designs": []}',
        test_case_context='{"test_cases": []}',
        rtm_context='{"coverage": []}',
        issues=["Risk strategy issue"],
        required_changes=["Correct risk assessment"],
        retry_count=1,
    )


def build_valid_route():
    return {
        "document_name": "sample.docx",
        "routes": [
            {
                "artifact": "RISK_STRATEGY",
                "route": "risk_strategy",
                "reason": "Risk strategy issue",
                "actions": ["Correct risk assessment"],
            }
        ],
    }


def test_risk_strategy_rework_handler_updates_context():
    fake_service = FakeRiskStrategyReworkService()

    handler = RiskStrategyReworkHandler(
        rework_service=fake_service
    )

    request = build_request()

    current_context = {
        "risk_strategy_context": (
            '{"strategy_summary": "Current strategy"}'
        )
    }

    updated_context = handler.handle(
        request=request,
        rework_result=None,
        routing_result=build_valid_route(),
        current_context=current_context,
    )

    assert "risk_strategy_context" in updated_context
    assert "Reworked strategy" in updated_context["risk_strategy_context"]

    assert fake_service.received_args is not None


def test_risk_strategy_rework_handler_passes_correct_request_data():
    fake_service = FakeRiskStrategyReworkService()

    handler = RiskStrategyReworkHandler(
        rework_service=fake_service
    )

    request = build_request()

    current_context = {
        "risk_strategy_context": (
            '{"strategy_summary": "Current strategy"}'
        )
    }

    handler.handle(
        request=request,
        rework_result=None,
        routing_result=build_valid_route(),
        current_context=current_context,
    )

    received = fake_service.received_args

    assert received["document_name"] == "sample.docx"
    assert received["requirement_context"] == '{"requirements": []}'
    assert received["current_strategy"] == (
        '{"strategy_summary": "Current strategy"}'
    )
    assert received["issues"] == ["Risk strategy issue"]
    assert received["required_changes"] == [
        "Correct risk assessment"
    ]
    assert received["retry_count"] == 1


def test_risk_strategy_rework_handler_rejects_wrong_artifact_route():
    handler = RiskStrategyReworkHandler(
        rework_service=FakeRiskStrategyReworkService()
    )

    request = build_request()

    current_context = {
        "risk_strategy_context": "{}"
    }

    wrong_route = {
        "document_name": "sample.docx",
        "routes": [
            {
                "artifact": "SCENARIOS",
                "route": "scenario_validation",
            }
        ],
    }

    try:
        handler.handle(
            request=request,
            rework_result=None,
            routing_result=wrong_route,
            current_context=current_context,
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "RISK_STRATEGY route" in str(exc)


def test_risk_strategy_rework_handler_rejects_wrong_strategy_route():
    handler = RiskStrategyReworkHandler(
        rework_service=FakeRiskStrategyReworkService()
    )

    request = build_request()

    current_context = {
        "risk_strategy_context": "{}"
    }

    wrong_route = {
        "document_name": "sample.docx",
        "routes": [
            {
                "artifact": "RISK_STRATEGY",
                "route": "scenario_validation",
            }
        ],
    }

    try:
        handler.handle(
            request=request,
            rework_result=None,
            routing_result=wrong_route,
            current_context=current_context,
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "risk_strategy" in str(exc)
