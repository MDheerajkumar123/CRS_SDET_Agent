from .config import PROVIDER_CONFIG, MAX_RETRIES
from .router import (
    get_provider_for_task,
    get_fallback_provider,
)
from .providers import (
    GeminiProvider,
    GroqProvider,
    OpenRouterProvider,
)
from .models import LLMResponse


class LLMManager:

    def __init__(self):
        self.providers = {
            "gemini": GeminiProvider(),
            "groq": GroqProvider(),
            "openrouter": OpenRouterProvider(),
        }

    def _generate_with_provider(
        self,
        provider_name: str,
        prompt: str,
    ) -> str:
        """
        Generate a response using one provider with retries.
        """

        provider = self.providers[provider_name]
        model = PROVIDER_CONFIG[provider_name]["model"]

        last_error = None

        for attempt in range(1, MAX_RETRIES + 1):

            try:
                response = provider.generate(
                    prompt=prompt,
                    model=model,
                )

                if not response:
                    raise ValueError(
                        f"{provider_name} returned an empty response."
                    )

                return response

            except Exception as error:
                last_error = error

                print(
                    f"[LLMManager] "
                    f"{provider_name} attempt "
                    f"{attempt}/{MAX_RETRIES} failed: {error}"
                )

        raise RuntimeError(
            f"{provider_name} failed after "
            f"{MAX_RETRIES} attempts."
        ) from last_error

    def generate(
        self,
        task_name: str,
        prompt: str,
    ) -> LLMResponse:
        """
        Generate an LLM response using the task's
        primary provider and controlled fallback.
        """

        primary_provider = get_provider_for_task(task_name)

        try:
            content = self._generate_with_provider(
                primary_provider,
                prompt,
            )

            return LLMResponse(
                content=content,
                provider=primary_provider,
                model=PROVIDER_CONFIG[primary_provider]["model"],
                task=task_name,
                fallback_used=False,
            )

        except Exception:

            print(
                f"[LLMManager] Primary provider "
                f"'{primary_provider}' failed."
            )

            fallback_provider = get_fallback_provider(
                primary_provider
            )

            print(
                f"[LLMManager] Switching to fallback "
                f"provider '{fallback_provider}'."
            )

            content = self._generate_with_provider(
                fallback_provider,
                prompt,
            )

            return LLMResponse(
                content=content,
                provider=fallback_provider,
                model=PROVIDER_CONFIG[fallback_provider]["model"],
                task=task_name,
                fallback_used=True,
            )
