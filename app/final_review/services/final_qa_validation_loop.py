from typing import Callable

from app.final_review.models.loop_result import (
    FinalQAValidationLoopResult,
)
from app.final_review.models.rework_request import (
    FinalQAReworkRequest,
)
from app.final_review.models.review_result import (
    FinalReviewStatus,
)
from app.final_review.models.rework_routing import (
    ReworkRoutingResult,
    ReworkTarget,
)
from app.final_review.services.final_qa_rework_dispatcher import (
    FinalQAReworkDispatcher,
)
from app.final_review.services.final_qa_rework_router import (
    FinalQAReworkRouter,
)
from app.final_review.services.final_qa_rework_service import (
    FinalQAReworkService,
)
from app.final_review.services.final_qa_reviewer_service import (
    FinalQAReviewerService,
)


class FinalQAValidationLoop:
    def __init__(
        self,
        reviewer_service=None,
        rework_service=None,
        rework_handler: Callable | None = None,
        router=None,
        dispatcher: FinalQAReworkDispatcher | None = None,
        max_retries: int = 3,
    ):
        self.reviewer_service = (
            reviewer_service or FinalQAReviewerService()
        )

        self.rework_service = (
            rework_service or FinalQAReworkService()
        )

        self.rework_handler = rework_handler

        self.router = router or FinalQAReworkRouter()

        self.dispatcher = dispatcher

        self.max_retries = max_retries

    def run(
        self,
        document_name: str,
        requirement_context: str,
        risk_strategy_context: str,
        scenario_context: str,
        test_design_context: str,
        test_case_context: str,
        rtm_context: str,
    ) -> FinalQAValidationLoopResult:

        current_context = {
            "requirement_context": requirement_context,
            "risk_strategy_context": risk_strategy_context,
            "scenario_context": scenario_context,
            "test_design_context": test_design_context,
            "test_case_context": test_case_context,
            "rtm_context": rtm_context,
        }

        retry_count = 0

        while True:

            # ---------------------------------------------------------
            # 1. Final QA Review
            # ---------------------------------------------------------
            review = self.reviewer_service.review(
                document_name=document_name,
                requirement_context=current_context[
                    "requirement_context"
                ],
                risk_strategy_context=current_context[
                    "risk_strategy_context"
                ],
                scenario_context=current_context[
                    "scenario_context"
                ],
                test_design_context=current_context[
                    "test_design_context"
                ],
                test_case_context=current_context[
                    "test_case_context"
                ],
                rtm_context=current_context[
                    "rtm_context"
                ],
            )

            # ---------------------------------------------------------
            # TEMPORARY DIAGNOSTIC OUTPUT
            # ---------------------------------------------------------
            # This allows us to see the exact Final QA reviewer
            # decision before the workflow continues.
            print("\n" + "=" * 70)
            print("FINAL QA REVIEW RESULT")
            print("=" * 70)
            print(f"STATUS: {review.status}")
            print(f"SCORE: {review.score}")
            print(f"ISSUES: {review.issues}")
            print(
                f"REQUIRED CHANGES: "
                f"{review.required_changes}"
            )
            print(
                f"SUMMARY: "
                f"{review.review_summary}"
            )
            print(f"RETRY COUNT: {retry_count}")
            print(f"MAX RETRIES: {self.max_retries}")
            print("=" * 70)
            print("END FINAL QA REVIEW RESULT")
            print("=" * 70 + "\n")

            # ---------------------------------------------------------
            # 2. PASS
            # ---------------------------------------------------------
            if review.status == FinalReviewStatus.PASS:
                return FinalQAValidationLoopResult(
                    final_review=review,
                    final_rework_request=None,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=True,
                )

            # ---------------------------------------------------------
            # 3. Maximum retry reached
            # ---------------------------------------------------------
            if retry_count >= self.max_retries:
                request = self._build_rework_request(
                    document_name=document_name,
                    current_context=current_context,
                    issues=review.issues,
                    required_changes=review.required_changes,
                    retry_count=retry_count,
                )

                return FinalQAValidationLoopResult(
                    final_review=review,
                    final_rework_request=request,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=False,
                )

            retry_count += 1

            # ---------------------------------------------------------
            # 4. Build rework request
            # ---------------------------------------------------------
            request = self._build_rework_request(
                document_name=document_name,
                current_context=current_context,
                issues=review.issues,
                required_changes=review.required_changes,
                retry_count=retry_count,
            )

            # ---------------------------------------------------------
            # 5. Identify rework targets
            # ---------------------------------------------------------
            rework_result = self.rework_service.rework(request)

            # ---------------------------------------------------------
            # 6. Convert rework targets into routing decisions
            # ---------------------------------------------------------
            routing_result = self.router.route(
                ReworkRoutingResult(
                    document_name=rework_result.document_name,
                    targets=[
                        ReworkTarget.model_validate(
                            target.model_dump()
                        )
                        for target in rework_result.rework_targets
                    ],
                    routing_summary=(
                        rework_result.overall_rework_summary
                    ),
                )
            )

            # ---------------------------------------------------------
            # 7. Resolve handler
            #
            # Backward compatibility:
            #
            # If an explicit rework_handler was supplied, preserve
            # the existing behavior used by the current tests and
            # callers.
            #
            # Otherwise, use the dispatcher to select the handler
            # based on the routed artifact.
            # ---------------------------------------------------------
            handler = self._resolve_handler(
                routing_result=routing_result
            )

            if handler is None:
                return FinalQAValidationLoopResult(
                    final_review=review,
                    final_rework_request=request,
                    retry_count=retry_count,
                    max_retries=self.max_retries,
                    passed=False,
                )

            # ---------------------------------------------------------
            # 8. Execute routed rework
            # ---------------------------------------------------------
            updated_context = handler(
                request,
                rework_result,
                routing_result,
                current_context,
            )

            if not isinstance(updated_context, dict):
                raise TypeError(
                    "rework handler must return a dictionary "
                    "containing updated QA artifact contexts."
                )

            # ---------------------------------------------------------
            # 9. Merge updated artifact contexts
            # ---------------------------------------------------------
            current_context.update(updated_context)

    def _build_rework_request(
        self,
        document_name: str,
        current_context: dict,
        issues: list[str],
        required_changes: list[str],
        retry_count: int,
    ) -> FinalQAReworkRequest:
        return FinalQAReworkRequest(
            document_name=document_name,
            requirement_context=current_context[
                "requirement_context"
            ],
            risk_strategy_context=current_context[
                "risk_strategy_context"
            ],
            scenario_context=current_context[
                "scenario_context"
            ],
            test_design_context=current_context[
                "test_design_context"
            ],
            test_case_context=current_context[
                "test_case_context"
            ],
            rtm_context=current_context[
                "rtm_context"
            ],
            issues=issues,
            required_changes=required_changes,
            retry_count=retry_count,
        )

    def _resolve_handler(
        self,
        routing_result: dict,
    ):
        # Existing explicit handler takes precedence.
        if self.rework_handler is not None:
            return self.rework_handler

        # No dispatcher means no automatic handler resolution.
        if self.dispatcher is None:
            return None

        routes = routing_result.get("routes")

        if not isinstance(routes, list) or not routes:
            return None

        if len(routes) != 1:
            raise ValueError(
                "Final QA rework currently requires exactly "
                "one routed artifact."
            )

        route = routes[0]

        handler = self.dispatcher.get_handler_for_route(
            route
        )

        if not hasattr(handler, "handle"):
            raise TypeError(
                "Registered Final QA rework handler must "
                "provide a handle method."
            )

        return handler.handle