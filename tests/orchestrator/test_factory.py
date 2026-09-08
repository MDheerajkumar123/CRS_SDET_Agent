from app.orchestrator.factory import create_crs_workflow
from app.orchestrator.workflow import CRSWorkflow


def test_create_crs_workflow():
    workflow = create_crs_workflow()

    assert isinstance(workflow, CRSWorkflow)

    dependencies = [
        "ingestion_pipeline",
        "requirement_analyzer",
        "requirement_validator_loop",
        "strategy_service",
        "scenario_service",
        "scenario_validator_loop",
        "test_design_service",
        "test_case_service",
        "test_case_validator_loop",
        "rtm_service",
        "rtm_validator_loop",
        "final_qa_loop",
        "excel_generator",
    ]

    for dependency in dependencies:
        assert getattr(workflow, dependency, None) is not None, (
            f"Missing workflow dependency: {dependency}"
        )

    assert len(dependencies) == 13
