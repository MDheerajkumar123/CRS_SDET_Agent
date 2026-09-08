from app.test_case.models.test_case import (
    TestCaseAnalysis,
)
from app.test_case.validation.models.rework_request import (
    TestCaseReworkRequest,
)
from app.test_case.validation.services.test_case_rework_service import (
    TestCaseReworkService,
)


class FakeResponse:
    content = """
    {
        "document_name": "Sample_CRS.docx",
        "test_case_summary": "Reworked test cases",
        "test_cases": [
            {
                "test_case_id": "TC-001",
                "design_id": "TD-001",
                "scenario_id": "SCN-001",
                "requirement_id": "REQ-001",
                "title": "Verify valid login",
                "objective": "Verify successful login",
                "test_type": "Functional",
                "priority": "High",
                "preconditions": [
                    "Valid user account exists"
                ],
                "test_data": [
                    "Valid user credentials"
                ],
                "steps": [
                    "Enter valid username",
                    "Enter valid password",
                    "Select Login"
                ],
                "expected_results": [
                    "User is successfully logged in"
                ],
                "source_design": "TD-001"
            }
        ],
        "overall_test_case_confidence": 0.95
    }
    """


class FakeLLMManager:
    def generate(self, task_name, prompt):
        assert task_name == "test_case"
        assert "Sample_CRS.docx" in prompt
        assert "Unsupported implementation assumption" in prompt
        assert "Remove unsupported assumption" in prompt
        return FakeResponse()


def test_test_case_rework_service():
    request = TestCaseReworkRequest(
        document_name="Sample_CRS.docx",
        current_test_cases="Current test cases JSON",
        issues=["Unsupported implementation assumption"],
        required_changes=["Remove unsupported assumption"],
        retry_count=1,
    )

    service = TestCaseReworkService(
        llm_manager=FakeLLMManager()
    )

    result = service.rework(request)

    assert isinstance(result, TestCaseAnalysis)
    assert result.document_name == "Sample_CRS.docx"
    assert len(result.test_cases) == 1
    assert result.test_cases[0].test_case_id == "TC-001"
    assert result.test_cases[0].requirement_id == "REQ-001"
    assert result.overall_test_case_confidence == 0.95

    print("Test Test Case Rework Service PASS")
