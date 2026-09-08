
from app.analysis.models.requirement import RequirementAnalysis
from app.validation.models.review_result import ReviewResult


def build_rework_prompt(
    analysis: RequirementAnalysis,
    review: ReviewResult,
) -> str:
    analysis_json = analysis.model_dump_json(indent=2)

    issues = "\n".join(
        f"- {issue}"
        for issue in review.issues
    ) or "- No issues provided."

    required_changes = "\n".join(
        f"- {change}"
        for change in review.required_changes
    ) or "- No required changes provided."

    return f"""
You are a Senior SDET Requirement Analysis Agent performing a
controlled rework cycle.

Your previous RequirementAnalysis was reviewed by an independent
Requirement Validation Reviewer.

Your task is to revise the analysis ONLY where the reviewer identified
a valid issue or required change.

IMPORTANT RULES:

- Preserve all valid requirements from the previous analysis.
- Do not invent CRS requirements.
- Do not add unsupported business rules, dependencies, acceptance
  criteria, error behavior, or non-functional requirements.
- Preserve source traceability.
- Every requirement ID must be unique.
- Correct duplicate or conflicting IDs when required.
- Preserve the distinction between Explicit, Inferred, Ambiguous,
  and Missing information.
- Do not present inferred information as Explicit.
- Add dependency information only when it is supported by the
  available CRS evidence.
- Do not remove valid information merely to satisfy formatting.
- Address every reviewer issue and required change.
- Return the complete revised RequirementAnalysis, not only the changes.

REQUIREMENT TYPE RULE:

Every requirement_type MUST use exactly one of the following allowed
values:

- Functional
- Non-Functional
- Business Rule
- Error/Exception
- QA Scope
- Payment Status
- User Role
- Data Requirement
- Dependency
- Traceability

Do NOT create new requirement_type values.

For example, do NOT use:
- Stakeholder Enumeration
- Scope Definition
- Scope Boundary
- Process
- Validation
- Business Process
- Stakeholder
- Feature
- Workflow

If a requirement does not clearly fit a specialized type, use the
most appropriate value from the allowed list above, based only on the
CRS evidence.

REQUIREMENT CLASSIFICATION RULE:

Every classification MUST use exactly one of:

- Explicit
- Inferred
- Ambiguous
- Missing

Do NOT create additional classification values.

REVIEWER STATUS:
{review.status.value}

REVIEWER SCORE:
{review.score}

REVIEWER ISSUES:
{issues}

REQUIRED CHANGES:
{required_changes}

PREVIOUS REQUIREMENT ANALYSIS:

{analysis_json}

OUTPUT REQUIREMENT:

Return ONLY valid JSON conforming exactly to the RequirementAnalysis
schema used by the CRS Analyzer.

The JSON must contain:

- document_name
- analysis_summary
- requirements
- overall_confidence

Each requirement must contain:

- requirement_id
- title
- description
- requirement_type
- classification
- source_document
- source_section
- source_page
- source_text
- business_rules
- dependencies
- confidence

Do not use Markdown.
Do not use code fences.
Do not include explanations outside the JSON.
""".strip()
