
from app.rtm.models.rtm import RTMAnalysis
from app.rtm.validation.models.loop_result import (
    RTMValidationLoopResult,
)
from app.rtm.validation.models.rework_request import (
    RTMReworkRequest,
)
from app.rtm.validation.models.review_result import (
    RTMReviewResult,
    RTMReviewStatus,
)
from app.rtm.validation.services.rtm_rework_service import (
    RTMReworkService,
)
from app.rtm.validation.services.rtm_validator_service import (
    RTMValidatorService,
)


class RTMValidationLoop:
    def __init__(
        self,
        validator_service=None,
        rework_service=None,
        max_retries: int = 3,
        event_publisher=None,
    ):
        self.validator_service = (
            validator_service or RTMValidatorService()
        )
        self.rework_service = (
            rework_service or RTMReworkService()
        )
        self.max_retries = max_retries
        self.event_publisher = event_publisher

    def _emit(self, event_type, **metadata):
        if self.event_publisher:
            self.event_publisher({"event_type": event_type, "stage": "RTM Validator", "message": "RTM validation requires rework." if event_type == "REWORK_STARTED" else "RTM artifact reworked.", "metadata": metadata})

    def run(
        self,
        document_name: str,
        requirement_context: str,
        scenario_context: str,
        test_design_context: str,
        test_case_context: str,
        rtm_analysis: RTMAnalysis,
    ) -> RTMValidationLoopResult:
        current_rtm = rtm_analysis
        retry_count = 0

        while True:
            review = self.validator_service.validate(
                document_name=document_name,
                requirement_context=requirement_context,
                scenario_context=scenario_context,
                test_design_context=test_design_context,
                test_case_context=test_case_context,
                rtm_analysis=current_rtm,
            )

            if review.status == RTMReviewStatus.PASS:
                return RTMValidationLoopResult(
                    final_rtm=current_rtm,
                    final_review=review,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=True,
                )

            if retry_count >= self.max_retries:
                return RTMValidationLoopResult(
                    final_rtm=current_rtm,
                    final_review=review,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=False,
                )

            retry_count += 1
            self._emit("REWORK_STARTED", attempt=retry_count, issues=review.issues, score=getattr(review, "score", None))

            request = RTMReworkRequest(
                document_name=document_name,
                current_rtm=current_rtm.model_dump_json(
                    indent=2
                ),
                issues=review.issues,
                required_changes=review.required_changes,
                retry_count=retry_count,
            )

            current_rtm = self.rework_service.rework(request)
            self._emit("REWORK_COMPLETED", attempt=retry_count)
