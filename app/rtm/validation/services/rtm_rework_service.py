
import json

from app.llm.manager import LLMManager
from app.rtm.models.rtm import RTMAnalysis
from app.rtm.validation.models.rework_request import RTMReworkRequest
from app.rtm.validation.prompts.rework_prompt import (
    build_rtm_rework_prompt,
)


class RTMReworkService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def rework(
        self,
        request: RTMReworkRequest,
    ) -> RTMAnalysis:
        if not isinstance(request, RTMReworkRequest):
            raise TypeError(
                "request must be an RTMReworkRequest instance."
            )

        prompt = build_rtm_rework_prompt(
            document_name=request.document_name,
            current_rtm=request.current_rtm,
            issues=request.issues,
            required_changes=request.required_changes,
            retry_count=request.retry_count,
        )

        response = self.llm_manager.generate(
            task_name="rtm",
            prompt=prompt,
        )

        content = response.content.strip()

        if content.startswith("```"):
            lines = content.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            content = "\n".join(lines).strip()

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "RTM rework returned invalid JSON."
            ) from exc

        return RTMAnalysis.model_validate(data)
