
from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.final_review.services.handlers.test_design_rework_handler import (
    TestDesignReworkHandler,
)
from app.test_design.models.test_design import (
    TestDesignAnalysis,
)


class FakeTestDesignReworkService:
    def __init__(self):
        self.received_args = None

    def rework(
        self,
        document_name,
        requirement_context,
        risk_strategy_context,
        scenario_context,
        current_design_context,
        issues,
        required_changes,
        retry_count,
    ):
        self.received_args = {
            "document_name": document_name,
            "requirement_context": requirement_context,
            "risk_strategy_context": risk_strategy_context,
            "scenario_context": scenario_context,
            "current_design_context": current_design_context,
            "issues": issues,
            "required_changes": required_changes,
            "retry_count": retry_count,
        }

        return TestDesignAnalysis(
            document_name=document_name,
            design_summary="Reworked test design",
            test_designs=[],
            overall_design_confidence=0.9,
        )


def build_request():
    return FinalQAReworkRequest(
        document_name="sample.docx",
        requirement_context='{"requirements": []}',
        risk_strategy_context='{"strategy": "risk"}',
        scenario_context='{"scenarios": []}',
        test_design_context='{"test_designs": []}',
        test_case_context='{"test_cases": []}',
        rtm_context='{"coverage": []}',
        issues=["Test design issue"],
        required_changes=["Correct design"],
        retry_count=1,
    )


def build_valid_route():
    return {
        "document_name": "sample.docx",
        "routes": [
            {
                "artifact": "TEST_DESIGNS",
                "route": "test_design",
                "reason": "Test design issue",
                "actions": ["Correct design"],
            }
        ],
    }


def test_test_design_rework_handler_updates_context():
    fake_service = FakeTestDesignReworkService()

    handler = TestDesignReworkHandler(
        rework_service=fake_service
    )

    request = build_request()

    current_context = {
        "test_design_context": '{"test_designs": []}'
    }

    updated_context = handler.handle(
        request=request,
        rework_result=None,
        routing_result=build_valid_route(),
        current_context=current_context,
    )

    assert "test_design_context" in updated_context
    assert "Reworked test design" in (
        updated_context["test_design_context"]
    )

    assert fake_service.received_args is not None


def test_test_design_rework_handler_passes_correct_request_data():
    fake_service = FakeTestDesignReworkService()

    handler = TestDesignReworkHandler(
        rework_service=fake_service
    )

    request = build_request()

    current_context = {
        "test_design_context": '{"test_designs": []}'
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
    assert received["risk_strategy_context"] == '{"strategy": "risk"}'
    assert received["scenario_context"] == '{"scenarios": []}'
    assert received["current_design_context"] == (
        '{"test_designs": []}'
    )
    assert received["issues"] == ["Test design issue"]
    assert received["required_changes"] == ["Correct design"]
    assert received["retry_count"] == 1


def test_test_design_rework_handler_rejects_wrong_artifact_route():
    handler = TestDesignReworkHandler(
        rework_service=FakeTestDesignReworkService()
    )

    request = build_request()

    current_context = {
        "test_design_context": "{}"
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
        assert "TEST_DESIGNS route" in str(exc)


def test_test_design_rework_handler_rejects_wrong_design_route():
    handler = TestDesignReworkHandler(
        rework_service=FakeTestDesignReworkService()
    )

    request = build_request()

    current_context = {
        "test_design_context": "{}"
    }

    wrong_route = {
        "document_name": "sample.docx",
        "routes": [
            {
                "artifact": "TEST_DESIGNS",
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
        assert "test_design" in str(exc)
