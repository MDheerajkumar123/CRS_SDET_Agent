from app.crew.crs_analyzer_crew import CRSAnalyzerCrew


DOCUMENT_NAME = "SmartBank_BRD_ERD_AI_Practice_New.docx"


def test_real_requirement_analyzer():
    crew = CRSAnalyzerCrew(
        document_name=DOCUMENT_NAME,
        query=(
            "Identify all testable requirements, business rules, "
            "errors, dependencies, and QA-relevant requirements."
        ),
        n_results=5,
    )

    result = crew.kickoff()

    print("\n===== RAW ANALYZER RESULT =====")
    print(result.raw)
    print("===== END RAW ANALYZER RESULT =====")

    assert result.raw