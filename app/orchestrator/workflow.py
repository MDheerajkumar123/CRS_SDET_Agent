
from typing import Any

from pydantic import BaseModel

from app.analysis.models.requirement import RequirementAnalysis
from app.strategy.models.test_strategy import TestStrategy
from app.scenario.models.test_scenario import ScenarioAnalysis
from app.test_design.models.test_design import TestDesignAnalysis
from app.test_case.models.test_case import TestCaseAnalysis
from app.rtm.models.rtm import RTMAnalysis
from app.final_review.models.review_result import FinalQAReviewResult


class CRSWorkflowResult(BaseModel):
    """
    Final result produced by the end-to-end CRS SDET workflow.
    """

    ingestion_result: Any

    requirement_analysis: RequirementAnalysis
    test_strategy: TestStrategy
    scenario_analysis: ScenarioAnalysis
    test_design_analysis: TestDesignAnalysis
    test_case_analysis: TestCaseAnalysis
    rtm_analysis: RTMAnalysis

    final_review: FinalQAReviewResult

    excel_path: str | None = None
    workflow_passed: bool


class CRSWorkflowInput(BaseModel):
    """
    Input required to execute the CRS SDET workflow.
    """

    file_path: str
    analysis_query: str
    n_results: int = 5
    output_path: str = "output/crs_sdet_qa.xlsx"


class CRSWorkflow:
    """
    End-to-end CRS-to-validated-QA-artifacts workflow.

    Workflow:

        1. Ingestion
        2. Requirement Analysis
        3. Requirement Validation
        4. Risk & Test Strategy
        5. Scenario Generation
        6. Scenario Validation
        7. Test Design Generation
        8. Test Case Generation
        9. Test Case Validation
        10. RTM Generation
        11. RTM Validation
        12. Final QA Review
        13. Excel Generation

    All services are dependency-injected so the workflow can be tested
    independently from real LLM/API services.
    """

    def __init__(
        self,
        ingestion_pipeline=None,
        requirement_analyzer=None,
        strategy_service=None,
        scenario_service=None,
        test_design_service=None,
        test_case_service=None,
        rtm_service=None,
        final_qa_loop=None,
        excel_generator=None,
        requirement_validator_loop=None,
        scenario_validator_loop=None,
        test_case_validator_loop=None,
        rtm_validator_loop=None,
    ):
        self.ingestion_pipeline = ingestion_pipeline
        self.requirement_analyzer = requirement_analyzer
        self.strategy_service = strategy_service
        self.scenario_service = scenario_service
        self.test_design_service = test_design_service
        self.test_case_service = test_case_service
        self.rtm_service = rtm_service
        self.final_qa_loop = final_qa_loop
        self.excel_generator = excel_generator

        self.requirement_validator_loop = requirement_validator_loop
        self.scenario_validator_loop = scenario_validator_loop
        self.test_case_validator_loop = test_case_validator_loop
        self.rtm_validator_loop = rtm_validator_loop

    # ============================================================
    # Context Helpers
    # ============================================================

    @staticmethod
    def _artifact_context(artifact) -> str:
        """
        Serialize a Pydantic artifact into formatted JSON context.

        This context is passed between downstream agents/services.
        """
        if artifact is None:
            raise ValueError("Artifact cannot be None.")

        if not hasattr(artifact, "model_dump_json"):
            raise TypeError(
                f"Expected a Pydantic model, got {type(artifact).__name__}."
            )

        return artifact.model_dump_json(indent=2)

    @staticmethod
    def _requirement_context(
        analysis: RequirementAnalysis,
    ) -> str:
        """
        Serialize requirement analysis into downstream context.
        """
        return CRSWorkflow._artifact_context(analysis)

    # ============================================================
    # Stage 1 - Ingestion
    # ============================================================

    def ingest(
        self,
        workflow_input: CRSWorkflowInput,
    ):
        if self.ingestion_pipeline is None:
            raise RuntimeError(
                "Ingestion pipeline is not configured."
            )

        return self.ingestion_pipeline.ingest(
            workflow_input.file_path
        )

    # ============================================================
    # Stage 2 - Requirement Analysis
    # ============================================================

    def analyze_requirements(
        self,
        workflow_input: CRSWorkflowInput,
        ingestion_result,
    ):
        if self.requirement_analyzer is None:
            raise RuntimeError(
                "Requirement analyzer is not configured."
            )

        return self.requirement_analyzer.analyze(
            document_name=ingestion_result.document_name,
            query=workflow_input.analysis_query,
            n_results=workflow_input.n_results,
        )

    # ============================================================
    # Stage 3 - Requirement Validation
    # ============================================================

    def validate_requirements(
        self,
        requirement_analysis: RequirementAnalysis,
    ):
        if self.requirement_validator_loop is None:
            raise RuntimeError(
                "Requirement validation loop is not configured."
            )

        return self.requirement_validator_loop.run(
            requirement_analysis
        )

    # ============================================================
    # Stage 4 - Risk & Test Strategy
    # ============================================================

    def generate_strategy(
        self,
        requirement_analysis: RequirementAnalysis,
    ) -> TestStrategy:
        if self.strategy_service is None:
            raise RuntimeError(
                "Strategy service is not configured."
            )

        return self.strategy_service.generate_strategy(
            requirement_analysis
        )

    # ============================================================
    # Stage 5 - Scenario Generation
    # ============================================================

    def generate_scenarios(
        self,
        requirement_analysis: RequirementAnalysis,
        strategy: TestStrategy,
    ) -> ScenarioAnalysis:
        if self.scenario_service is None:
            raise RuntimeError(
                "Scenario service is not configured."
            )

        return self.scenario_service.generate_scenarios(
            requirement_analysis,
            strategy,
        )

    # ============================================================
    # Stage 6 - Scenario Validation
    # ============================================================

    def validate_scenarios(
        self,
        requirement_analysis: RequirementAnalysis,
        strategy: TestStrategy,
        scenario_analysis: ScenarioAnalysis,
    ):
        if self.scenario_validator_loop is None:
            raise RuntimeError(
                "Scenario validation loop is not configured."
            )

        return self.scenario_validator_loop.run(
            analysis=requirement_analysis,
            strategy=strategy,
            scenarios=scenario_analysis,
            requirement_context=self._requirement_context(
                requirement_analysis
            ),
            risk_strategy_context=self._artifact_context(
                strategy
            ),
        )

    # ============================================================
    # Stage 7 - Test Design Generation
    # ============================================================

    def generate_test_designs(
        self,
        requirement_analysis: RequirementAnalysis,
        strategy: TestStrategy,
        scenario_analysis: ScenarioAnalysis,
    ) -> TestDesignAnalysis:
        if self.test_design_service is None:
            raise RuntimeError(
                "Test design service is not configured."
            )

        return self.test_design_service.generate_designs(
            requirement_analysis,
            strategy,
            scenario_analysis,
        )

    # ============================================================
    # Stage 8 - Test Case Generation
    # ============================================================

    def generate_test_cases(
        self,
        requirement_analysis: RequirementAnalysis,
        strategy: TestStrategy,
        scenario_analysis: ScenarioAnalysis,
        test_design_analysis: TestDesignAnalysis,
    ) -> TestCaseAnalysis:
        if self.test_case_service is None:
            raise RuntimeError(
                "Test case service is not configured."
            )

        return self.test_case_service.generate_test_cases(
            requirement_analysis,
            strategy,
            scenario_analysis,
            test_design_analysis,
        )

    # ============================================================
    # Stage 9 - Test Case Validation
    # ============================================================

    def validate_test_cases(
        self,
        document_name: str,
        requirement_analysis: RequirementAnalysis,
        strategy: TestStrategy,
        scenario_analysis: ScenarioAnalysis,
        test_design_analysis: TestDesignAnalysis,
        test_case_analysis: TestCaseAnalysis,
    ):
        if self.test_case_validator_loop is None:
            raise RuntimeError(
                "Test case validation loop is not configured."
            )

        return self.test_case_validator_loop.run(
            document_name=document_name,
            requirement_context=self._artifact_context(
                requirement_analysis
            ),
            risk_strategy_context=self._artifact_context(
                strategy
            ),
            scenario_context=self._artifact_context(
                scenario_analysis
            ),
            test_design_context=self._artifact_context(
                test_design_analysis
            ),
            test_case_analysis=test_case_analysis,
        )

    # ============================================================
    # Stage 10 - RTM Generation
    # ============================================================

    def generate_rtm(
        self,
        document_name: str,
        requirement_analysis: RequirementAnalysis,
        scenario_analysis: ScenarioAnalysis,
        test_design_analysis: TestDesignAnalysis,
        test_case_analysis: TestCaseAnalysis,
    ) -> RTMAnalysis:
        if self.rtm_service is None:
            raise RuntimeError(
                "RTM service is not configured."
            )

        return self.rtm_service.generate(
            document_name=document_name,
            requirement_context=self._artifact_context(
                requirement_analysis
            ),
            scenario_context=self._artifact_context(
                scenario_analysis
            ),
            test_design_context=self._artifact_context(
                test_design_analysis
            ),
            test_case_context=self._artifact_context(
                test_case_analysis
            ),
        )

    # ============================================================
    # Stage 11 - RTM Validation
    # ============================================================

    def validate_rtm(
        self,
        document_name: str,
        requirement_analysis: RequirementAnalysis,
        scenario_analysis: ScenarioAnalysis,
        test_design_analysis: TestDesignAnalysis,
        test_case_analysis: TestCaseAnalysis,
        rtm_analysis: RTMAnalysis,
    ):
        if self.rtm_validator_loop is None:
            raise RuntimeError(
                "RTM validation loop is not configured."
            )

        return self.rtm_validator_loop.run(
            document_name=document_name,
            requirement_context=self._artifact_context(
                requirement_analysis
            ),
            scenario_context=self._artifact_context(
                scenario_analysis
            ),
            test_design_context=self._artifact_context(
                test_design_analysis
            ),
            test_case_context=self._artifact_context(
                test_case_analysis
            ),
            rtm_analysis=rtm_analysis,
        )

    # ============================================================
    # Stage 12 - Final QA Review
    # ============================================================

    def run_final_qa(
        self,
        document_name: str,
        requirement_analysis: RequirementAnalysis,
        strategy: TestStrategy,
        scenario_analysis: ScenarioAnalysis,
        test_design_analysis: TestDesignAnalysis,
        test_case_analysis: TestCaseAnalysis,
        rtm_analysis: RTMAnalysis,
    ):
        if self.final_qa_loop is None:
            raise RuntimeError(
                "Final QA validation loop is not configured."
            )

        return self.final_qa_loop.run(
            document_name=document_name,
            requirement_context=self._artifact_context(
                requirement_analysis
            ),
            risk_strategy_context=self._artifact_context(
                strategy
            ),
            scenario_context=self._artifact_context(
                scenario_analysis
            ),
            test_design_context=self._artifact_context(
                test_design_analysis
            ),
            test_case_context=self._artifact_context(
                test_case_analysis
            ),
            rtm_context=self._artifact_context(
                rtm_analysis
            ),
        )

    # ============================================================
    # Stage 13 - Excel Generation
    # ============================================================

    def generate_excel(
        self,
        requirement_analysis: RequirementAnalysis,
        strategy: TestStrategy,
        scenario_analysis: ScenarioAnalysis,
        test_design_analysis: TestDesignAnalysis,
        test_case_analysis: TestCaseAnalysis,
        rtm_analysis: RTMAnalysis,
        output_path: str,
    ):
        if self.excel_generator is None:
            raise RuntimeError(
                "Excel generator is not configured."
            )

        from app.excel.excel_generator import ExcelGeneratorInput

        data = ExcelGeneratorInput(
            requirement_analysis=requirement_analysis,
            test_strategy=strategy,
            scenario_analysis=scenario_analysis,
            test_design_analysis=test_design_analysis,
            test_case_analysis=test_case_analysis,
            rtm_analysis=rtm_analysis,
        )

        return self.excel_generator.generate(
            data=data,
            output_path=output_path,
        )

    # ============================================================
    # End-to-End Workflow
    # ============================================================

    def run(
        self,
        workflow_input: CRSWorkflowInput,
    ) -> CRSWorkflowResult:
        """
        Execute the complete CRS SDET workflow.
        """

        # --------------------------------------------------------
        # 1. Ingestion
        # --------------------------------------------------------

        ingestion_result = self.ingest(
            workflow_input
        )

        # --------------------------------------------------------
        # 2. Requirement Analysis
        # --------------------------------------------------------

        requirement_analysis, _ = self.analyze_requirements(
            workflow_input,
            ingestion_result,
        )

        # --------------------------------------------------------
        # 3. Requirement Validation
        # --------------------------------------------------------

        requirement_validation = self.validate_requirements(
            requirement_analysis
        )

        if not requirement_validation.passed:
            raise RuntimeError(
                "Requirement validation failed."
            )

        requirement_analysis = (
            requirement_validation.final_analysis
        )

        # --------------------------------------------------------
        # 4. Risk & Test Strategy
        # --------------------------------------------------------

        strategy = self.generate_strategy(
            requirement_analysis
        )

        # --------------------------------------------------------
        # 5. Scenario Generation
        # --------------------------------------------------------

        scenario_analysis = self.generate_scenarios(
            requirement_analysis,
            strategy,
        )

        # --------------------------------------------------------
        # 6. Scenario Validation
        # --------------------------------------------------------

        scenario_validation = self.validate_scenarios(
            requirement_analysis,
            strategy,
            scenario_analysis,
        )

        if not scenario_validation.passed:
            review = scenario_validation.final_review

            print("\n=== FINAL SCENARIO VALIDATION REVIEW ===")
            print("STATUS:", review.status.value)
            print("SCORE:", review.score)
            print("ISSUES:", review.issues)
            print("REQUIRED CHANGES:", review.required_changes)
            print("RETRY COUNT:", scenario_validation.retry_count)
            print("MAX RETRIES:", scenario_validation.max_retries)
            print("=== END FINAL SCENARIO VALIDATION REVIEW ===\n")

            raise RuntimeError(
                "Scenario validation failed."
            )

        scenario_analysis = (
            scenario_validation.final_scenarios
        )

        # --------------------------------------------------------
        # 7. Test Design Generation
        # --------------------------------------------------------

        test_design_analysis = self.generate_test_designs(
            requirement_analysis,
            strategy,
            scenario_analysis,
        )

        # --------------------------------------------------------
        # 8. Test Case Generation
        # --------------------------------------------------------

        test_case_analysis = self.generate_test_cases(
            requirement_analysis,
            strategy,
            scenario_analysis,
            test_design_analysis,
        )

        # --------------------------------------------------------
        # 9. Test Case Validation
        # --------------------------------------------------------

        test_case_validation = self.validate_test_cases(
            document_name=requirement_analysis.document_name,
            requirement_analysis=requirement_analysis,
            strategy=strategy,
            scenario_analysis=scenario_analysis,
            test_design_analysis=test_design_analysis,
            test_case_analysis=test_case_analysis,
        )

        if not test_case_validation.passed:
            raise RuntimeError(
                "Test case validation failed."
            )

        test_case_analysis = (
            test_case_validation.final_test_cases
        )

        # --------------------------------------------------------
        # 10. RTM Generation
        # --------------------------------------------------------

        rtm_analysis = self.generate_rtm(
            document_name=requirement_analysis.document_name,
            requirement_analysis=requirement_analysis,
            scenario_analysis=scenario_analysis,
            test_design_analysis=test_design_analysis,
            test_case_analysis=test_case_analysis,
        )

        # --------------------------------------------------------
        # 11. RTM Validation
        # --------------------------------------------------------

        rtm_validation = self.validate_rtm(
            document_name=requirement_analysis.document_name,
            requirement_analysis=requirement_analysis,
            scenario_analysis=scenario_analysis,
            test_design_analysis=test_design_analysis,
            test_case_analysis=test_case_analysis,
            rtm_analysis=rtm_analysis,
        )

        if not rtm_validation.passed:
            raise RuntimeError(
                "RTM validation failed."
            )

        rtm_analysis = (
            rtm_validation.final_rtm
        )

        # --------------------------------------------------------
        # 12. Final QA Review
        # --------------------------------------------------------

        final_qa = self.run_final_qa(
            document_name=requirement_analysis.document_name,
            requirement_analysis=requirement_analysis,
            strategy=strategy,
            scenario_analysis=scenario_analysis,
            test_design_analysis=test_design_analysis,
            test_case_analysis=test_case_analysis,
            rtm_analysis=rtm_analysis,
        )

        if not final_qa.passed:
            raise RuntimeError(
                "Final QA validation failed."
            )

        # --------------------------------------------------------
        # 13. Excel Generation
        # --------------------------------------------------------

        excel_path = self.generate_excel(
            requirement_analysis=requirement_analysis,
            strategy=strategy,
            scenario_analysis=scenario_analysis,
            test_design_analysis=test_design_analysis,
            test_case_analysis=test_case_analysis,
            rtm_analysis=rtm_analysis,
            output_path=workflow_input.output_path,
        )

        # --------------------------------------------------------
        # Final Result
        # --------------------------------------------------------

        return CRSWorkflowResult(
            ingestion_result=ingestion_result,
            requirement_analysis=requirement_analysis,
            test_strategy=strategy,
            scenario_analysis=scenario_analysis,
            test_design_analysis=test_design_analysis,
            test_case_analysis=test_case_analysis,
            rtm_analysis=rtm_analysis,
            final_review=final_qa.final_review,
            excel_path=str(excel_path),
            workflow_passed=True,
        )
