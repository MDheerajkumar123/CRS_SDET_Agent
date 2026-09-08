from app.analysis.models.requirement import RequirementAnalysis


def build_requirement_validation_prompt(
    analysis: RequirementAnalysis,
) -> str:
    analysis_json = analysis.model_dump_json(indent=2)

    return f"""
You are a Senior SDET Requirement Validation Reviewer.

Your responsibility is to REVIEW the supplied requirement analysis.
Do not rewrite, improve, or invent requirements.

Validate the analysis against these criteria:

1. Requirement completeness
2. Requirement classification correctness
3. Hallucination and unsupported inference
4. Source traceability
5. Duplicate requirements
6. Business-rule traceability
7. Dependency validity
8. Requirement testability
9. Missing or ambiguous requirements
10. Confidence score validity

IMPORTANT RULES:

- Use only the information contained in the supplied RequirementAnalysis.
- Do not invent CRS facts.
- Do not add requirements that are not supported by the analysis.
- Do not modify requirement IDs.
- Do not silently correct descriptions.
- Distinguish explicit information from inferred information.
- Flag statements that appear more specific than their source evidence supports.
- Check that source_document and source_section are populated.
- Check that business rules referenced by requirements are valid.
- Check that dependencies are meaningful and not fabricated.
- Check for duplicate or substantially overlapping requirements.
- Check whether each requirement is testable.
- Check confidence values are between 0 and 1.
- Identify potentially missing or ambiguous requirements only when the analysis itself provides evidence for the concern.

REVIEW DECISION:

Return PASS when the analysis is sufficiently accurate and traceable.

Return REWORK when material issues require the CRS Analyzer to revise its output.

SCORING:

90-100 = Excellent
80-89  = Good but minor issues
70-79  = Material issues requiring review
Below 70 = Significant issues requiring rework

OUTPUT FORMAT:

Return ONLY valid JSON.
Do not use Markdown.
Do not use code fences.

The JSON must exactly follow this structure:

{{
    "status": "PASS",
    "score": 0,
    "issues": [],
    "required_changes": []
}}

Allowed status values:
- PASS
- REWORK

Requirement Analysis to review:

{analysis_json}
""".strip()
