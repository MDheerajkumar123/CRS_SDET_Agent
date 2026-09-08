
import json

from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.final_review.services.handlers.test_case_rework_handler import (
    TestCaseReworkHandler,
)
from app.test_case.models.test_case import (
    TestCaseAnalysis,
)


class FakeTestCaseReworkService:
    def __init__(self):
        self.received_request = None

    def rework(self, request):
        self.received_request = request

        return TestCaseAnalysis(
            document_name=request.document_name,
            test_case_summary="Reworked test cases.",
            test_cases=[],
            overall_test_case_confidence=0.95,
        )


def build_request():
    return FinalQAReworkRequest(
        document_name="sample.docx",
        requirement_context="REQ-001",
        risk_strategy_context="REQ-001 risk",
        scenario_context="SCN-001",
        test_design_context="TD-001",
        test_case_context='{"test_cases": []}',
        rtm_context="REQ-001 Covered",
        issues=["Coverage gap"],
        required_changes=["Add missing test coverage."],
        retry_count=1,
    )


def test_test_case_rework_handler_updates_test_case_context():
    fake_service = FakeTestCaseReworkService()

    handler = TestCaseReworkHandler(
        rework_service=fake_service
    )

    request = build_request()

    current_context = {
        "requirement_context": "REQ-001",
        "risk_strategy_context": "REQ-001 risk",
        "scenario_context": "SCN-001",
        "test_design_context": "TD-001",
        "test_case_context": '{"test_cases": []}',
        "rtm_context": "REQ-001 Covered",
    }

    result = handler.handle(
        request=request,
        rework_result=None,
        routing_result={
            "document_name": "sample.docx",
            "routes": [
                {
                    "artifact": "TEST_CASES",
                    "route": "test_case_validation",
                }
            ],
        },
        current_context=current_context,
    )

    assert "test_case_context" in result

    parsed = json.loads(
        result["test_case_context"]
    )

    assert parsed["document_name"] == "sample.docx"
    assert parsed["test_case_summary"] == (
        "Reworked test cases."
    )


def test_test_case_rework_handler_builds_correct_request():
    fake_service = FakeTestCaseReworkService()

    handler = TestCaseReworkHandler(
        rework_service=fake_service
    )

    request = build_request()

    current_context = {
        "test_case_context": '{"existing": "test cases"}'
    }

    handler.handle(
        request=request,
        rework_result=None,
        routing_result={
            "document_name": "sample.docx",
            "routes": [
                {
                    "artifact": "TEST_CASES",
                    "route": "test_case_validation",
                }
            ],
        },
        current_context=current_context,
    )

    received = fake_service.received_request

    assert received is not None
    assert received.document_name == "sample.docx"
    assert received.current_test_cases == (
        '{"existing": "test cases"}'
    )
    assert received.issues == ["Coverage gap"]
    assert received.required_changes == [
        "Add missing test coverage."
    ]
    assert received.retry_count == 1


def test_test_case_rework_handler_rejects_missing_context():
    handler = TestCaseReworkHandler(
        rework_service=FakeTestCaseReworkService()
    )

    request = build_request()

    try:
        handler.handle(
            request=request,
            rework_result=None,
            routing_result={
                "document_name": "sample.docx",
                "routes": [
                    {
                        "artifact": "TEST_CASES",
                        "route": "test_case_validation",
                    }
                ],
            },
            current_context={},
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "test_case_context" in str(exc)

def test_test_case_rework_handler_rejects_wrong_artifact_route():
    handler = TestCaseReworkHandler(
        rework_service=FakeTestCaseReworkService()
    )

    request = build_request()

    current_context = {
        "test_case_context": '{"test_cases": []}'
    }

    try:
        handler.handle(
            request=request,
            rework_result=None,
            routing_result={
                "document_name": "sample.docx",
                "routes": [
                    {
                        "artifact": "SCENARIOS",
                        "route": "scenario_validation",
                    }
                ],
            },
            current_context=current_context,
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "TEST_CASES route" in str(exc)


def test_test_case_rework_handler_rejects_wrong_test_case_route():
    handler = TestCaseReworkHandler(
        rework_service=FakeTestCaseReworkService()
    )

    request = build_request()

    current_context = {
        "test_case_context": '{"test_cases": []}'
    }

    try:
        handler.handle(
            request=request,
            rework_result=None,
            routing_result={
                "document_name": "sample.docx",
                "routes": [
                    {
                        "artifact": "TEST_CASES",
                        "route": "scenario_validation",
                    }
                ],
            },
            current_context=current_context,
        )
        assert False, "Expected ValueError"
    except ValueError as exc:
        assert "test_case_validation" in str(exc)
