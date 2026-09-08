
from app.analysis.models.requirement import (
    RequirementAnalysis,
)
from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.final_review.services.handlers.requirement_rework_handler import (
    RequirementReworkHandler,
)
from app.validation.models.review_result import (
    ReviewResult,
    ReviewStatus,
)


class FakeRequirementReworkService:
    def __init__(self):
        self.received_analysis = None
        self.received_review = None

    def rework(self, analysis, review):
        self.received_analysis = analysis
        self.received_review = review

        return analysis, None


def build_request():
    return FinalQAReworkRequest(
        document_name="sample.docx",
        requirement_context=(
            '{"document_name": "sample.docx", '
            '"analysis_summary": "Current analysis", '
            '"requirements": [], '
            '"overall_confidence": 0.9}'
        ),
        risk_strategy_context='{"strategy_summary": "Strategy"}',
        scenario_context='{"scenarios": []}',
        test_design_context='{"test_designs": []}',
        test_case_context='{"test_cases": []}',
        rtm_context='{"coverage": []}',
        issues=["Requirement issue"],
        required_changes=["Correct requirement"],
        retry_count=1,
    )


def build_valid_route():
    return {
        "document_name": "sample.docx",
        "routes": [
            {
                "artifact": "REQUIREMENTS",
                "route": "requirement_validation",
                "reason": "Requirement issue",
                "actions": ["Correct requirement"],
            }
        ],
    }


def build_requirement_context():
    analysis = RequirementAnalysis(
        document_name="sample.docx",
        analysis_summary="Current analysis",
        requirements=[],
        overall_confidence=0.9,
    )

    return analysis.model_dump_json(indent=2)


def test_requirement_rework_handler_updates_context():
    fake_service = FakeRequirementReworkService()

    handler = RequirementReworkHandler(
        rework_service=fake_service
    )

    request = build_request()

    current_context = {
        "requirement_context": build_requirement_context()
    }

    updated_context = handler.handle(
        request=request,
        rework_result=None,
        routing_result=build_valid_route(),
        current_context=current_context,
    )

    assert "requirement_context" in updated_context
    assert "sample.docx" in updated_context["requirement_context"]

    assert isinstance(
        fake_service.received_analysis,
        RequirementAnalysis,
    )


def test_requirement_rework_handler_builds_correct_review():
    fake_service = FakeRequirementReworkService()

    handler = RequirementReworkHandler(
        rework_service=fake_service
    )

    request = build_request()

    current_context = {
        "requirement_context": build_requirement_context()
    }

    handler.handle(
        request=request,
        rework_result=None,
        routing_result=build_valid_route(),
        current_context=current_context,
    )

    review = fake_service.received_review

    assert isinstance(review, ReviewResult)
    assert review.status == ReviewStatus.REWORK
    assert review.score == 0
    assert review.issues == ["Requirement issue"]
    assert review.required_changes == ["Correct requirement"]


def test_requirement_rework_handler_rejects_wrong_artifact_route():
    handler = RequirementReworkHandler(
        rework_service=FakeRequirementReworkService()
    )

    request = build_request()

    current_context = {
        "requirement_context": build_requirement_context()
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
        assert "REQUIREMENTS route" in str(exc)


def test_requirement_rework_handler_rejects_wrong_requirement_route():
    handler = RequirementReworkHandler(
        rework_service=FakeRequirementReworkService()
    )

    request = build_request()

    current_context = {
        "requirement_context": build_requirement_context()
    }

    wrong_route = {
        "document_name": "sample.docx",
        "routes": [
            {
                "artifact": "REQUIREMENTS",
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
        assert "requirement_validation" in str(exc)
