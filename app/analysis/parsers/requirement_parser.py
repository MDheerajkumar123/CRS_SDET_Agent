import json

from app.analysis.models.requirement import RequirementAnalysis


class RequirementAnalysisParser:
    """
    Converts raw LLM output into a validated RequirementAnalysis object.
    """

    @staticmethod
    def parse(raw_response: str) -> RequirementAnalysis:
        if not raw_response or not raw_response.strip():
            raise ValueError("LLM response is empty.")

        cleaned_response = raw_response.strip()

        # Handle markdown JSON fences such as:
        # ```json
        # {...}
        # ```
        if cleaned_response.startswith("```"):
            lines = cleaned_response.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned_response = "\n".join(lines).strip()

        try:
            data = json.loads(cleaned_response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"LLM response is not valid JSON: {exc}"
            ) from exc

        try:
            return RequirementAnalysis.model_validate(data)
        except Exception as exc:
            raise ValueError(
                f"LLM JSON does not conform to RequirementAnalysis schema: {exc}"
            ) from exc
