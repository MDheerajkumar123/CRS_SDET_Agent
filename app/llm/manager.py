from openai import RateLimitError
from groq import APIStatusError as GroqAPIStatusError
from groq import RateLimitError as GroqRateLimitError
from google.genai import errors

from .config import (
    PROVIDER_CONFIG,
    MAX_EMPTY_RESPONSE_RETRIES,
    MAX_RETRIES,
)
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


RATE_LIMIT_ERRORS = (
    RateLimitError,
    GroqRateLimitError,
)


class EmptyLLMResponseError(ValueError):
    """Raised when a provider responds without usable generated content."""


class LLMManager:

    def __init__(self):
        self.providers = {
            "gemini": GeminiProvider(),
            "groq": GroqProvider(),
            "openrouter": OpenRouterProvider(),
        }

    @staticmethod
    def _is_rate_limit_error(error: Exception) -> bool:
        if isinstance(error, RATE_LIMIT_ERRORS):
            return True

        if isinstance(error, GroqAPIStatusError):
            error_body = getattr(error, "body", {}) or {}
            error_data = error_body.get("error", {}) if isinstance(error_body, dict) else {}
            return (
                getattr(error, "status_code", None) == 429
                or error_data.get("code") == "rate_limit_exceeded"
            )

        if isinstance(error, errors.ClientError):
            return getattr(error, "code", None) == 429

        return False
    def _generate_with_provider(
        self,
        provider_name: str,
        prompt: str,
    ) -> str:
        """
        Generate a response using one provider with retries.

        Rate-limit/quota errors are not retried because the
        condition is unlikely to recover during this call.
        """

        provider = self.providers[provider_name]
        model = PROVIDER_CONFIG[provider_name]["model"]

        last_error = None

        attempt_limit = MAX_RETRIES

        for attempt in range(1, attempt_limit + 1):

            try:
                response = provider.generate(
                    prompt=prompt,
                    model=model,
                )

                if not isinstance(response, str) or not response.strip():
                    raise EmptyLLMResponseError(
                        f"{provider_name} returned an empty response."
                    )

                return response

            except Exception as error:
                last_error = error

                print(
                    f"[LLMManager] "
                    f"{provider_name} attempt "
                    f"{attempt}/{attempt_limit} failed: {error}"
                )

                if isinstance(error, EmptyLLMResponseError):
                    # A repeated empty completion consumes quota without
                    # evidence that the provider has recovered. Move to the
                    # ordered fallback after the conservative configured limit.
                    attempt_limit = min(
                        attempt_limit,
                        max(1, MAX_EMPTY_RESPONSE_RETRIES),
                    )

                    if attempt >= attempt_limit:
                        break

                if self._is_rate_limit_error(error):
                    print(
                        f"[LLMManager] "
                        f"{provider_name} rate limit/quota detected. "
                        f"Skipping remaining retries."
                    )
                    break

        raise RuntimeError(
            f"{provider_name} failed after "
            f"{attempt_limit} attempts."
        ) from last_error

    def generate(
        self,
        task_name: str,
        prompt: str,
    ) -> LLMResponse:
        """
        Generate an LLM response using the task's
        primary provider and ordered fallback providers.
        """

        primary_provider = get_provider_for_task(task_name)

        providers_to_try = [
            primary_provider,
            *get_fallback_provider(primary_provider),
        ]

        last_error = None

        for index, provider_name in enumerate(providers_to_try):

            try:
                content = self._generate_with_provider(
                    provider_name,
                    prompt,
                )

                return LLMResponse(
                    content=content,
                    provider=provider_name,
                    model=PROVIDER_CONFIG[provider_name]["model"],
                    task=task_name,
                    fallback_used=(index > 0),
                )

            except Exception as error:
                last_error = error

                if index < len(providers_to_try) - 1:
                    print(
                        f"[LLMManager] Provider "
                        f"'{provider_name}' failed."
                    )
                    print(
                        f"[LLMManager] Switching to fallback "
                        f"provider '{providers_to_try[index + 1]}'."
                    )

        raise RuntimeError(
            f"All configured providers failed for task "
            f"'{task_name}'."
        ) from last_error
