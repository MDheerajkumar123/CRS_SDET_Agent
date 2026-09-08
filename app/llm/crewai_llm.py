from crewai import LLM

from app.llm.config import PROVIDER_CONFIG


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
            return LLM(
                model=model,
                provider="openai",
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1",
                temperature=temperature,
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
