import json

import pytest

from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.final_review.services.handlers.rtm_rework_handler import (
    RTMReworkHandler,
)
from app.rtm.models.rtm import RTMAnalysis
from app.rtm.validation.models.rework_request import (
    RTMReworkRequest,
)


class FakeRTMReworkService:
    def __init__(self):
        self.received_request = None

    def rework(self, request):
        self.received_request = request

        return RTMAnalysis(
            document_name=request.document_name,
            rtm_summary="Reworked RTM",
            requirement_coverage=[],
            total_requirements=0,
            covered_requirements=0,
            partially_covered_requirements=0,
            not_covered_requirements=0,
            overall_coverage_percentage=0.0,
        )


def make_request():
    return FinalQAReworkRequest(
        document_name="SmartBank.docx",
        requirement_context="requirements",
        risk_strategy_context="risk strategy",
        scenario_context="scenarios",
        test_design_context="test designs",
        test_case_context="test cases",
        rtm_context="current rtm",
        issues=["RTM coverage issue"],
        required_changes=["Fix RTM coverage"],
        retry_count=1,
    )


def make_routing_result():
    return {
        "document_name": "SmartBank.docx",
        "routes": [
            {
                "artifact": "RTM",
                "route": "rtm_validation",
                "reason": "RTM requires rework",
                "actions": ["Fix RTM coverage"],
            }
        ],
    }


def test_rtm_handler_reworks_and_updates_context():
    service = FakeRTMReworkService()
    handler = RTMReworkHandler(rework_service=service)

    result = handler.handle(
        request=make_request(),
        rework_result=None,
        routing_result=make_routing_result(),
        current_context={
            "rtm_context": "current rtm"
        },
    )

    assert "rtm_context" in result

    updated_rtm = json.loads(result["rtm_context"])

    assert updated_rtm["document_name"] == "SmartBank.docx"
    assert updated_rtm["rtm_summary"] == "Reworked RTM"

    assert isinstance(
        service.received_request,
        RTMReworkRequest,
    )

    assert service.received_request.current_rtm == "current rtm"
    assert service.received_request.issues == [
        "RTM coverage issue"
    ]
    assert service.received_request.required_changes == [
        "Fix RTM coverage"
    ]
    assert service.received_request.retry_count == 1


def test_rtm_handler_rejects_missing_rtm_context():
    handler = RTMReworkHandler(
        rework_service=FakeRTMReworkService()
    )

    with pytest.raises(ValueError, match="rtm_context"):
        handler.handle(
            request=make_request(),
            rework_result=None,
            routing_result=make_routing_result(),
            current_context={},
        )


def test_rtm_handler_rejects_missing_rtm_route():
    handler = RTMReworkHandler(
        rework_service=FakeRTMReworkService()
    )

    routing_result = {
        "document_name": "SmartBank.docx",
        "routes": [],
    }

    with pytest.raises(ValueError, match="RTM route"):
        handler.handle(
            request=make_request(),
            rework_result=None,
            routing_result=routing_result,
            current_context={
                "rtm_context": "current rtm"
            },
        )


def test_rtm_handler_rejects_wrong_rtm_route():
    handler = RTMReworkHandler(
        rework_service=FakeRTMReworkService()
    )

    routing_result = {
        "document_name": "SmartBank.docx",
        "routes": [
            {
                "artifact": "RTM",
                "route": "wrong_route",
                "reason": "invalid route",
                "actions": [],
            }
        ],
    }

    with pytest.raises(
        ValueError,
        match="rtm_validation",
    ):
        handler.handle(
            request=make_request(),
            rework_result=None,
            routing_result=routing_result,
            current_context={
                "rtm_context": "current rtm"
            },
        )


def test_rtm_handler_rejects_invalid_request():
    handler = RTMReworkHandler(
        rework_service=FakeRTMReworkService()
    )

    with pytest.raises(
        TypeError,
        match="FinalQAReworkRequest",
    ):
        handler.handle(
            request={},
            rework_result=None,
            routing_result=make_routing_result(),
            current_context={
                "rtm_context": "current rtm"
            },
        )
