
from textwrap import dedent


def build_risk_strategy_rework_prompt(
    document_name: str,
    requirement_context: str,
    current_strategy: str,
    issues: list[str],
    required_changes: list[str],
    retry_count: int = 0,
) -> str:
    issues_text = "\n".join(
        f"- {issue}" for issue in issues
    ) or "- No specific issues supplied."

    changes_text = "\n".join(
        f"- {change}" for change in required_changes
    ) or "- No specific required changes supplied."

    return dedent(
        f"""
        You are a Senior SDET and Test Strategy Engineer performing
        controlled rework of an existing risk-based testing strategy.

        SOURCE DOCUMENT:
        {document_name}

        RETRY COUNT:
        {retry_count}

        VALIDATED REQUIREMENTS:
        {requirement_context}

        CURRENT TEST STRATEGY:
        {current_strategy}

        FINAL QA REVIEW ISSUES:
        {issues_text}

        REQUIRED CHANGES:
        {changes_text}

        OBJECTIVE:
        Correct only the identified problems in the current TestStrategy
        while preserving valid existing risk assessments, prioritization,
        traceability, and strategy information.

        IMPORTANT RULES:

        1. REQUIREMENT TRACEABILITY
           - Every RequirementRisk must reference an existing requirement_id
             from the supplied validated requirements.
           - Never invent requirement IDs.
           - Never create new business requirements.
           - Never change a requirement ID merely to resolve a review issue.

        2. RISK ASSESSMENT
           - Risk decisions must be based only on the supplied requirements.
           - Consider business impact, failure impact, security sensitivity,
             financial or transaction impact, data integrity, dependencies,
             user impact, regulatory/audit impact, performance/reliability,
             complexity, and ambiguity where supported by the requirements.
           - Do not invent implementation details.

        3. RISK LEVEL
           Use only:
           - Low
           - Medium
           - High
           - Critical

        4. RISK SCORE
           - Must be an integer from 1 to 100.
           - Higher scores represent greater testing risk.
           - Keep risk_score logically consistent with risk_level.

        5. RISK REASON
           - Make each reason specific to its requirement.
           - Do not add unsupported assumptions.

        6. IMPACTED AREAS
           - Use only areas supported by the requirement context.
           - Do not invent unsupported business or technical areas.

        7. TEST TYPES
           Use only these allowed values:
           - Functional
           - Negative
           - Boundary
           - Integration
           - Regression
           - Security
           - Performance
           - Usability
           - Compatibility
           - Reliability
           - Auditability

           Recommend a test type only when justified by the requirement.

        8. PRIORITIZATION
           - prioritized_requirements must contain only existing requirement IDs.
           - Higher-risk and higher-business-impact requirements should be
             prioritized appropriately.

        9. PRESERVE VALID INFORMATION
           - Do not rewrite unaffected strategy information unnecessarily.
           - Do not remove valid risk entries unless the supplied requirements
             clearly show that they are unsupported.
           - Correct identified issues while preserving valid traceability.

        10. NO HALLUCINATION
            - Do not invent requirements.
            - Do not invent business rules.
            - Do not invent dependencies.
            - Do not invent business areas.
            - Do not assume implementation details.
            - If information is insufficient, assess conservatively.

        11. CONFIDENCE
            overall_strategy_confidence must be between 0 and 1.
            Lower confidence when the supplied requirements do not provide
            enough information for reliable risk assessment.

        12. OVERALL RISK
            overall_risk_level must reflect the highest meaningful risk in
            the analyzed requirements, considering overall business impact.

        13. SCOPE
            Rework only the Risk & Test Strategy artifact.
            Do not generate scenarios, test designs, test cases, or RTM data.

        14. REVIEW ALIGNMENT
            Address the supplied Final QA issues and required changes.
            Do not introduce unrelated changes.

        OUTPUT REQUIREMENT:

        Return ONLY a valid JSON object conforming exactly to the
        TestStrategy schema.

        Do not return:
        - Markdown
        - Code fences
        - Explanations outside JSON
        - Comments
        - Additional fields

        Expected structure:

        {{
          "document_name": "string",
          "strategy_summary": "string",
          "requirement_risks": [
            {{
              "requirement_id": "string",
              "risk_level": "Low | Medium | High | Critical",
              "risk_score": 1,
              "risk_reason": "string",
              "impacted_areas": ["string"],
              "recommended_test_types": [
                "Functional | Negative | Boundary | Integration | Regression | Security | Performance | Usability | Compatibility | Reliability | Auditability"
              ]
            }}
          ],
          "prioritized_requirements": ["REQ-001"],
          "overall_risk_level": "Low | Medium | High | Critical",
          "overall_strategy_confidence": 0.0
        }}
        """
    )
