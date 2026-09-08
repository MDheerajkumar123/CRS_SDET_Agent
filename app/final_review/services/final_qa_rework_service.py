
import json

from app.final_review.models.rework_request import FinalQAReworkRequest
from app.final_review.prompts.rework_prompt import (
    build_final_qa_rework_prompt,
)
from app.llm.manager import LLMManager
from pydantic import BaseModel, Field


class ReworkTarget(BaseModel):
    artifact: str
    reason: str
    actions: list[str] = Field(default_factory=list)


class FinalQAReworkResult(BaseModel):
    document_name: str
    rework_targets: list[ReworkTarget] = Field(default_factory=list)
    overall_rework_summary: str


class FinalQAReworkService:
    def __init__(self, llm_manager=None):
        self.llm_manager = llm_manager or LLMManager()

    def rework(
        self,
        request: FinalQAReworkRequest,
    ) -> FinalQAReworkResult:
        if not isinstance(request, FinalQAReworkRequest):
            raise TypeError(
                "request must be a FinalQAReworkRequest instance."
            )

        prompt = build_final_qa_rework_prompt(
            document_name=request.document_name,
            requirement_context=request.requirement_context,
            risk_strategy_context=request.risk_strategy_context,
            scenario_context=request.scenario_context,
            test_design_context=request.test_design_context,
            test_case_context=request.test_case_context,
            rtm_context=request.rtm_context,
            issues=request.issues,
            required_changes=request.required_changes,
            retry_count=request.retry_count,
        )

        response = self.llm_manager.generate(
            task_name="final_reviewer",
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
                "Final QA rework returned invalid JSON."
            ) from exc

        return FinalQAReworkResult.model_validate(data)
