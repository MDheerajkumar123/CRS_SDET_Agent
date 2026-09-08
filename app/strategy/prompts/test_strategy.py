from textwrap import dedent


def build_test_strategy_prompt(
    document_name: str,
    requirement_context: str,
) -> str:
    return dedent(
        f"""
        You are a Senior SDET and Test Strategy Engineer.

        Your task is to analyze the validated requirements extracted from the
        Customer Requirement Specification (CRS) and produce a risk-based
        testing strategy.

        SOURCE DOCUMENT:
        {document_name}

        VALIDATED REQUIREMENTS:
        {requirement_context}

        OBJECTIVE:
        Identify testing risks, prioritize requirements, and recommend the
        appropriate test types for each requirement.

        IMPORTANT RULES:

        1. REQUIREMENT TRACEABILITY
           - Every RequirementRisk must reference an existing requirement_id.
           - Never invent requirement IDs.
           - Do not create new business requirements.
           - Base risk decisions only on the supplied validated requirements.

        2. RISK IDENTIFICATION
           Evaluate each relevant requirement for:
           - Business impact
           - Failure impact
           - Security sensitivity
           - Financial or transaction impact
           - Data integrity impact
           - Integration/dependency impact
           - User impact
           - Regulatory/audit impact
           - Performance/reliability impact
           - Complexity or ambiguity

        3. RISK LEVEL
           Use only:
           - Low
           - Medium
           - High
           - Critical

        4. RISK SCORE
           Assign an integer from 1 to 100.
           Higher scores must represent greater testing risk.

           Suggested guidance:
           - 1-25   = Low
           - 26-50  = Medium
           - 51-75  = High
           - 76-100 = Critical

           The score and risk level must be logically consistent.

        5. RISK REASON
           Explain why the requirement has the assigned risk.
           Keep the reason specific to the requirement.

        6. IMPACTED AREAS
           Identify relevant areas such as:
           - Payment processing
           - Authentication
           - Authorization
           - User experience
           - Data integrity
           - Integration
           - Security
           - Performance
           - Audit
           - Reliability

           Do not add unsupported business areas.

        7. TEST TYPES
           Recommend only test types that are justified by the requirement.

           Allowed values:
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

        8. TEST PRIORITIZATION
           prioritized_requirements must contain requirement IDs from the
           supplied requirements only.

           Place higher-risk and higher-business-impact requirements first.

        9. COVERAGE
           Consider all validated requirements when determining the overall
           testing strategy. Do not automatically assign a risk entry to
           every requirement if there is no meaningful testing risk, but do
           not omit important or high-risk requirements.

        10. NO HALLUCINATION
            - Do not invent requirements.
            - Do not invent business rules.
            - Do not invent dependencies.
            - Do not assume implementation details that are not present.
            - If information is insufficient, reflect that conservatively in
              the risk assessment.

        11. CONFIDENCE
            overall_strategy_confidence must be between 0 and 1.
            Lower confidence when requirements are ambiguous, incomplete, or
            provide insufficient information for risk assessment.

        12. OVERALL RISK
            overall_risk_level must reflect the highest meaningful risk in
            the analyzed requirements, considering overall business impact.

        OUTPUT REQUIREMENT:

        Return ONLY a valid JSON object conforming exactly to the TestStrategy
        schema.

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
