from app.orchestrator.workflow import CRSWorkflow

from app.llm.manager import LLMManager

from app.ingestion.pipeline import IngestionPipeline
from app.analysis.services.requirement_analyzer import RequirementAnalyzer
from app.strategy.services.test_strategy_service import TestStrategyService
from app.scenario.services.test_scenario_service import TestScenarioService
from app.test_design.services.test_design_service import TestDesignService
from app.test_case.services.test_case_service import TestCaseService
from app.rtm.services.rtm_service import RTMService

from app.validation.services.validation_loop import ValidationLoop

from app.scenario.validation.services.scenario_validation_loop import (
    ScenarioValidationLoop,
)

from app.test_case.validation.services.test_case_validation_loop import (
    TestCaseValidationLoop,
)

from app.test_case.validation.services.test_case_validator_service import (
    TestCaseValidatorService,
)

from app.test_case.validation.services.test_case_rework_service import (
    TestCaseReworkService,
)

from app.rtm.validation.services.rtm_validation_loop import (
    RTMValidationLoop,
)

from app.final_review.services.final_qa_validation_loop import (
    FinalQAValidationLoop,
)

from app.excel.excel_generator import ExcelGenerator


def create_crs_workflow() -> CRSWorkflow:
    """
    Create the production CRS SDET workflow with all
    real application dependencies configured.

    This function only constructs the application objects.
    It does not execute the CRS workflow.
    """

    # ------------------------------------------------------------
    # Shared LLM Manager
    # ------------------------------------------------------------

    llm_manager = LLMManager()

    # ------------------------------------------------------------
    # Core Services
    # ------------------------------------------------------------

    ingestion_pipeline = IngestionPipeline()

    requirement_analyzer = RequirementAnalyzer(
        llm_manager=llm_manager,
    )

    strategy_service = TestStrategyService(
        llm_manager=llm_manager,
    )

    scenario_service = TestScenarioService(
        llm_manager=llm_manager,
    )

    test_design_service = TestDesignService(
        llm_manager=llm_manager,
    )

    test_case_service = TestCaseService(
        llm_manager=llm_manager,
    )

    rtm_service = RTMService(
        llm_manager=llm_manager,
    )

    # ------------------------------------------------------------
    # Requirement Validation
    # ------------------------------------------------------------

    requirement_validator_loop = ValidationLoop()

    # ------------------------------------------------------------
    # Scenario Validation
    # ------------------------------------------------------------

    scenario_validator_loop = ScenarioValidationLoop()

    # ------------------------------------------------------------
    # Test Case Validation
    # ------------------------------------------------------------

    test_case_validator_service = TestCaseValidatorService(
        llm_manager=llm_manager,
    )

    test_case_rework_service = TestCaseReworkService(
        llm_manager=llm_manager,
    )

    test_case_validator_loop = TestCaseValidationLoop(
        validator_service=test_case_validator_service,
        rework_service=test_case_rework_service,
    )

    # ------------------------------------------------------------
    # RTM Validation
    # ------------------------------------------------------------

    rtm_validation_loop = RTMValidationLoop()

    # ------------------------------------------------------------
    # Final QA Validation
    # ------------------------------------------------------------

    final_qa_loop = FinalQAValidationLoop()

    # ------------------------------------------------------------
    # Deterministic Excel Generator
    # ------------------------------------------------------------

    excel_generator = ExcelGenerator()

    # ------------------------------------------------------------
    # Assemble Workflow
    # ------------------------------------------------------------

    return CRSWorkflow(
        ingestion_pipeline=ingestion_pipeline,
        requirement_analyzer=requirement_analyzer,

        strategy_service=strategy_service,

        scenario_service=scenario_service,

        test_design_service=test_design_service,

        test_case_service=test_case_service,

        rtm_service=rtm_service,

        requirement_validator_loop=requirement_validator_loop,

        scenario_validator_loop=scenario_validator_loop,

        test_case_validator_loop=test_case_validator_loop,

        rtm_validator_loop=rtm_validation_loop,

        final_qa_loop=final_qa_loop,

        excel_generator=excel_generator,
    )
