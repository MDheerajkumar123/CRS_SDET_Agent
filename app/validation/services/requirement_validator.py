
import json

from app.analysis.models.requirement import RequirementAnalysis
from app.llm.manager import LLMManager
from app.validation.models.review_result import ReviewResult
from app.validation.prompts.requirement_validator import (
    build_requirement_validation_prompt,
)


class RequirementValidator:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def validate(
        self,
        analysis: RequirementAnalysis,
    ) -> tuple[ReviewResult, object]:

        if not isinstance(analysis, RequirementAnalysis):
            raise TypeError(
                "analysis must be a RequirementAnalysis instance."
            )

        prompt = build_requirement_validation_prompt(analysis)

        llm_response = self.llm_manager.generate(
            task_name="requirement_reviewer",
            prompt=prompt,
        )

        review = self._parse_review_response(
            llm_response.content
        )

        return review, llm_response

    @staticmethod
    def _parse_review_response(
        raw_response: str,
    ) -> ReviewResult:

        if not raw_response or not raw_response.strip():
            raise ValueError("Reviewer LLM response is empty.")

        cleaned_response = raw_response.strip()

        # Remove Markdown code fences if the LLM returns them.
        if cleaned_response.startswith("```"):
            lines = cleaned_response.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            cleaned_response = "\n".join(lines).strip()

        # Parse JSON response.
        try:
            data = json.loads(cleaned_response)

        except json.JSONDecodeError as exc:
            # Some LLM responses may contain a valid JSON object
            # followed by additional text or another JSON fragment.
            # Extract the first complete JSON value safely.
            decoder = json.JSONDecoder()
            start = cleaned_response.find("{")

            if start == -1:
                raise ValueError(
                    f"Reviewer LLM response is not valid JSON: {exc}"
                ) from exc

            try:
                data, _ = decoder.raw_decode(
                    cleaned_response[start:]
                )

            except json.JSONDecodeError:
                raise ValueError(
                    f"Reviewer LLM response is not valid JSON: {exc}"
                ) from exc

        # Normalize structured issue objects returned by some LLMs
        # into the list[str] format required by ReviewResult.
        for field in ("issues", "required_changes"):
            values = data.get(field, [])

            if isinstance(values, list):
                data[field] = [
                    (
                        f"{item.get('type', 'Issue')}: "
                        f"{item.get('description', str(item))}"
                    )
                    if isinstance(item, dict)
                    else str(item)
                    for item in values
                ]

        # Validate the normalized response against the Pydantic model.
        try:
            return ReviewResult.model_validate(data)

        except Exception as exc:
            raise ValueError(
                "Reviewer response does not conform to "
                f"ReviewResult schema: {exc}"
            ) from exc
