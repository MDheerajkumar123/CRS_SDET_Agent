from pathlib import Path

from app.orchestrator.factory import create_crs_workflow
from app.orchestrator.workflow import CRSWorkflowInput


def main():
    input_file = Path("data/input/Sample.docx")
    output_file = Path("output/crs_sdet_qa.xlsx")

    if not input_file.exists():
        raise FileNotFoundError(f"CRS file not found: {input_file}")

    workflow = create_crs_workflow()

    workflow_input = CRSWorkflowInput(
        file_path=str(input_file),
        analysis_query="Analyze the CRS and identify all testable software requirements.",
        n_results=5,
        output_path=str(output_file),
    )

    result = workflow.run(workflow_input)

    print("\n=== CRS SDET AI Agent ===")
    print(f"Workflow passed: {result.workflow_passed}")
    print(f"Excel output: {result.excel_path}")

    if result.final_review:
        print(f"Final QA status: {result.final_review.status}")
        print(f"Final QA score: {result.final_review.score}")


if __name__ == "__main__":
    main()
