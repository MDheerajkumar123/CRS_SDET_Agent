from app.test_case.validation.models.rework_request import (
    TestCaseReworkRequest,
)


def test_test_case_rework_request_model():
    request = TestCaseReworkRequest(
        document_name="Sample_CRS.docx",
        current_test_cases="Current test cases JSON",
        issues=["Unsupported implementation assumption"],
        required_changes=["Remove unsupported assumption"],
        retry_count=1,
    )

    assert request.document_name == "Sample_CRS.docx"
    assert request.current_test_cases == "Current test cases JSON"
    assert request.issues == ["Unsupported implementation assumption"]
    assert request.required_changes == ["Remove unsupported assumption"]
    assert request.retry_count == 1

    print("Test Test Case Rework Request Model PASS")
