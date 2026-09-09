import json
import re

from app.scenario.models.test_scenario import ScenarioAnalysis


class ScenarioAnalysisParser:
    @staticmethod
    def parse(raw_response: str) -> ScenarioAnalysis:
        if not raw_response or not raw_response.strip():
            raise ValueError("LLM response is empty.")

        cleaned_response = raw_response.strip()

        # Remove Markdown JSON code fences.
        cleaned_response = re.sub(
            r"```(?:json)?\s*",
            "",
            cleaned_response,
            flags=re.IGNORECASE,
        )
        cleaned_response = cleaned_response.replace("```", "").strip()

        # Extract the JSON object from surrounding LLM commentary.
        start = cleaned_response.find("{")
        end = cleaned_response.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise ValueError(
                "LLM response does not contain a JSON object."
            )

        cleaned_response = cleaned_response[start:end + 1]

        # Remove C-style comments that some LLMs insert into JSON.
        cleaned_response = re.sub(
            r"/\*.*?\*/",
            "",
            cleaned_response,
            flags=re.DOTALL,
        )

        cleaned_response = re.sub(
            r"^\s*//.*$",
            "",
            cleaned_response,
            flags=re.MULTILINE,
        )

        # Convert JSON string to Python object.
        try:
            data = json.loads(cleaned_response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"LLM response is not valid JSON: {exc}"
            ) from exc

        # Validate against ScenarioAnalysis Pydantic model.
        try:
            return ScenarioAnalysis.model_validate(data)
        except Exception as exc:
            raise ValueError(
                "LLM JSON does not conform to ScenarioAnalysis schema: "
                f"{exc}"
            ) from exc