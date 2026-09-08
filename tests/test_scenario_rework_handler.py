
from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.final_review.services.handlers.scenario_rework_handler import (
    ScenarioReworkHandler,
)
from app.scenario.models.test_scenario import (
    ScenarioAnalysis,
    TestScenario,
)


class FakeScenarioReworkService:
    def __init__(self):
        self.received_args = None

    def rework(
        self,
        scenarios,
        review,
        document_name,
        requirement_context,
        risk_strategy_context,
    ):
        self.received_args = {
            "scenarios": scenarios,
            "review": review,
            "document_name": document_name,
            "requirement_context": requirement_context,
            "risk_strategy_context": risk_strategy_context,
        }

        return scenarios, None


def build_request():
    return FinalQAReworkRequest(
        document_name="sample.docx",
        requirement_context='{"requirements": []}',
        risk_strategy_context='{"risks": []}',
        scenario_context='{"scenarios": []}',
        test_design_context='{"test_designs": []}',
        test_case_context='{"test_cases": []}',
        rtm_context='{"coverage": []}',
        issues=["Scenario issue"],
        required_changes=["Fix scenario"],
        retry_count=1,
    )


def build_scenario_context():
    scenarios = ScenarioAnalysis(
        document_name="sample.docx",
        scenario_summary="Sample scenarios",
        scenarios=[],
        overall_scenario_confidence=0.9,
    )

    return scenarios.model_dump_json(indent=2)


def build_valid_route():
    return {
        "document_name": "sample.docx",
        "routes": [
            {
                "artifact": "SCENARIOS",
                "route": "scenario_validation",
                "reason": "Scenario issue",
                "actions": ["Fix scenario"],
            }
        ],
    }


def test_scenario_rework_handler_updates_scenario_context():
    fake_service = FakeScenarioReworkService()

    handler = ScenarioReworkHandler(
        rework_service=fake_service
    )

    request = build_request()

    current_context = {
        "scenario_context": build_scenario_context()
    }

    updated_context = handler.handle(
        request=request,
        rework_result=None,
        routing_result=build_valid_route(),
        current_context=current_context,
    )

    assert "scenario_context" in updated_context
    assert "sample.docx" in updated_context["scenario_context"]

    assert fake_service.received_args is not None
    assert isinstance(
        fake_service.received_args["scenarios"],
        ScenarioAnalysis,
    )


def test_scenario_rework_handler_passes_correct_request_data():
    fake_service = FakeScenarioReworkService()

    handler = ScenarioReworkHandler(
        rework_service=fake_service
    )

    request = build_request()

    current_context = {
        "scenario_context": build_scenario_context()
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
    assert received["risk_strategy_context"] == '{"risks": []}'
    assert received["review"].status.value == "REWORK"
    assert received["review"].issues == ["Scenario issue"]
    assert received["review"].required_changes == ["Fix scenario"]


def test_scenario_rework_handler_rejects_wrong_artifact_route():
    handler = ScenarioReworkHandler(
        rework_service=FakeScenarioReworkService()
    )

    request = build_request()

    current_context = {
        "scenario_context": build_scenario_context()
    }

    wrong_route = {
        "document_name": "sample.docx",
        "routes": [
            {
                "artifact": "TEST_CASES",
                "route": "test_case_validation",
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
        assert "SCENARIOS route" in str(exc)


def test_scenario_rework_handler_rejects_wrong_scenario_route():
    handler = ScenarioReworkHandler(
        rework_service=FakeScenarioReworkService()
    )

    request = build_request()

    current_context = {
        "scenario_context": build_scenario_context()
    }

    wrong_route = {
        "document_name": "sample.docx",
        "routes": [
            {
                "artifact": "SCENARIOS",
                "route": "test_case_validation",
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
        assert "scenario_validation" in str(exc)
