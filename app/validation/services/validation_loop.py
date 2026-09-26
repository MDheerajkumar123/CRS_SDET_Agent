from app.analysis.models.requirement import RequirementAnalysis
from app.validation.models.loop_result import ValidationLoopResult
from app.validation.models.review_result import (
    ReviewResult,
    ReviewStatus,
)
from app.validation.services.requirement_validator import (
    RequirementValidator,
)
from app.validation.services.rework_service import (
    RequirementReworkService,
)


class ValidationLoop:
    def __init__(
        self,
        validator=None,
        rework_service=None,
        max_retries: int = 3,
        event_publisher=None,
    ):
        if max_retries < 1:
            raise ValueError("max_retries must be at least 1.")

        self.validator = validator or RequirementValidator()
        self.rework_service = (
            rework_service or RequirementReworkService()
        )
        self.max_retries = max_retries
        self.event_publisher = event_publisher

    def _emit(self, event_type, **metadata):
        if self.event_publisher:
            self.event_publisher({"event_type": event_type, "stage": "Requirement Validator", "message": "Requirement validation requires rework." if event_type == "REWORK_STARTED" else "Requirement artifact reworked.", "metadata": metadata})

    def run(
        self,
        analysis: RequirementAnalysis,
    ) -> ValidationLoopResult:

        if not isinstance(analysis, RequirementAnalysis):
            raise TypeError(
                "analysis must be a RequirementAnalysis instance."
            )

        current_analysis = analysis
        retry_count = 0

        while True:
            review, _ = self.validator.validate(
                current_analysis
            )

            if review.status == ReviewStatus.PASS:
                return ValidationLoopResult(
                    final_analysis=current_analysis,
                    final_review=review,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=True,
                )

            if retry_count >= self.max_retries:
                return ValidationLoopResult(
                    final_analysis=current_analysis,
                    final_review=review,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=False,
                )

            self._emit("REWORK_STARTED", attempt=retry_count + 1, issues=review.issues, score=getattr(review, "score", None))
            current_analysis, _ = self.rework_service.rework(
                analysis=current_analysis,
                review=review,
            )

            retry_count += 1
            self._emit("REWORK_COMPLETED", attempt=retry_count)
