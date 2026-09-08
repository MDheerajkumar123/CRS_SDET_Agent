import json

from app.scenario.models.test_scenario import ScenarioAnalysis


class ScenarioAnalysisParser:
    @staticmethod
    def parse(raw_response: str) -> ScenarioAnalysis:
        if not raw_response or not raw_response.strip():
            raise ValueError("LLM response is empty.")

        cleaned_response = raw_response.strip()

        # Remove Markdown JSON code fences if the LLM returns:
        # ```json
        # {...}
        # ```
        if cleaned_response.startswith("```"):
            lines = cleaned_response.splitlines()

            if lines and lines[0].strip().startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned_response = "\n".join(lines).strip()

        # Convert JSON string to Python object
        try:
            data = json.loads(cleaned_response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"LLM response is not valid JSON: {exc}"
            ) from exc

        # Validate against ScenarioAnalysis Pydantic model
        try:
            return ScenarioAnalysis.model_validate(data)
        except Exception as exc:
            raise ValueError(
                "LLM JSON does not conform to ScenarioAnalysis schema: "
                f"{exc}"
            ) from exc
