from app.test_case.models.review_result import (
    TestCaseReviewResult,
    TestCaseReviewStatus,
)
from app.test_case.models.test_case import TestCaseAnalysis
from app.test_case.validation.models.loop_result import (
    TestCaseValidationLoopResult,
)
from app.test_case.validation.models.rework_request import (
    TestCaseReworkRequest,
)


class TestCaseValidationLoop:
    def __init__(
        self,
        validator_service,
        rework_service,
        max_retries: int = 3,
        event_publisher=None,
    ):
        self.validator_service = validator_service
        self.rework_service = rework_service
        self.max_retries = max_retries
        self.event_publisher = event_publisher

    def _emit(self, event_type, **metadata):
        if self.event_publisher:
            self.event_publisher({"event_type": event_type, "stage": "Test Case Validator", "message": "Test case validation requires rework." if event_type == "REWORK_STARTED" else "Test cases reworked.", "metadata": metadata})

    def run(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
        scenario_context: str,
        test_design_context: str,
        test_case_analysis: TestCaseAnalysis,
    ) -> TestCaseValidationLoopResult:

        if not isinstance(test_case_analysis, TestCaseAnalysis):
            raise TypeError(
                "test_case_analysis must be a TestCaseAnalysis instance"
            )

        current_test_cases = test_case_analysis
        retry_count = 0

        while True:
            review = self.validator_service.validate(
                document_name=document_name,
                requirement_context=requirement_context,
                risk_strategy_context=risk_strategy_context,
                scenario_context=scenario_context,
                test_design_context=test_design_context,
                test_case_analysis=current_test_cases,
            )

            if not isinstance(review, TestCaseReviewResult):
                raise TypeError(
                    "validator_service must return TestCaseReviewResult"
                )

            if review.status == TestCaseReviewStatus.PASS:
                return TestCaseValidationLoopResult(
                    final_test_cases=current_test_cases,
                    final_review=review,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=True,
                )

            if retry_count >= self.max_retries:
                return TestCaseValidationLoopResult(
                    final_test_cases=current_test_cases,
                    final_review=review,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=False,
                )

            retry_count += 1
            self._emit("REWORK_STARTED", attempt=retry_count, issues=review.issues, score=getattr(review, "score", None))

            rework_request = TestCaseReworkRequest(
                document_name=document_name,
                current_test_cases=current_test_cases.model_dump_json(
                    indent=2
                ),
                issues=review.issues,
                required_changes=review.required_changes,
                retry_count=retry_count,
            )

            current_test_cases = self.rework_service.rework(
                rework_request
            )
            self._emit("REWORK_COMPLETED", attempt=retry_count)

            if not isinstance(current_test_cases, TestCaseAnalysis):
                raise TypeError(
                    "rework_service must return TestCaseAnalysis"
                )
