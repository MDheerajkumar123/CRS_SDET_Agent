from typing import Any

from crewai import LLM
from crewai.llms.providers.openai.completion import OpenAICompletion
from pydantic import BaseModel

from app.llm.config import PROVIDER_CONFIG


class _OpenRouterJSONLLM(OpenAICompletion):
    """Use CrewAI's normal OpenRouter completion path for Pydantic tasks.

    CrewAI 1.15.18 routes ``response_model`` on its legacy ``LLM`` through
    ``InternalInstructor``. That path creates a fresh LiteLLM request using
    only the model name, losing this instance's OpenRouter base URL and API
    key. The task still retains ``output_pydantic``; CrewAI validates the
    returned JSON against that model after this normal completion returns.
    """

    def call(
        self,
        messages: str | list[dict[str, Any]],
        tools=None,
        callbacks=None,
        available_functions=None,
        from_task=None,
        from_agent=None,
        response_model: type[BaseModel] | None = None,
    ) -> str | Any:
        return super().call(
            messages=messages,
            tools=tools,
            callbacks=callbacks,
            available_functions=available_functions,
            from_task=from_task,
            from_agent=from_agent,
            response_model=None,
        )


class CrewAILLMFactory:
    """
    Creates CrewAI LLM instances from the project's existing
    provider configuration.
    """

    @staticmethod
    def create(
        provider_name: str = "openrouter",
        temperature: float = 0.0,
    ) -> LLM:
        if provider_name not in PROVIDER_CONFIG:
            raise ValueError(
                f"Unknown provider: {provider_name}"
            )

        config = PROVIDER_CONFIG[provider_name]

        api_key = config["api_key"]
        model = config["model"]

        if not api_key:
            raise ValueError(
                f"{provider_name.upper()}_API_KEY is not configured."
            )

        if not model:
            raise ValueError(
                f"{provider_name.upper()}_MODEL is not configured."
            )

        if provider_name == "openrouter":
            return _OpenRouterJSONLLM(
                model=model,
                provider="openai",
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                temperature=temperature,
                custom_openai=True,
            )

        if provider_name == "groq":
            return LLM(
                model=model,
                provider="groq",
                api_key=api_key,
                temperature=temperature,
            )

        if provider_name == "gemini":
            return LLM(
                model=model,
                provider="gemini",
                api_key=api_key,
                temperature=temperature,
            )

        raise ValueError(
            f"Unsupported CrewAI provider: {provider_name}"
        )
