import app.llm.manager as manager_module
from app.llm.manager import LLMManager


class FakeProvider:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def generate(self, prompt, model):
        self.calls += 1
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def test_empty_or_whitespace_response_uses_fallback_without_extra_retries(
    monkeypatch,
):
    openrouter = FakeProvider(["   "])
    gemini = FakeProvider(["fallback response"])
    groq = FakeProvider(["unused"])

    manager = object.__new__(LLMManager)
    manager.providers = {
        "openrouter": openrouter,
        "gemini": gemini,
        "groq": groq,
    }

    monkeypatch.setattr(
        manager_module,
        "PROVIDER_CONFIG",
        {
            name: {"model": f"{name}-model"}
            for name in manager.providers
        },
    )
    monkeypatch.setattr(manager_module, "MAX_RETRIES", 3)
    monkeypatch.setattr(manager_module, "MAX_EMPTY_RESPONSE_RETRIES", 1)

    response = manager.generate(
        task_name="test_case_validator",
        prompt="test prompt",
    )

    assert response.content == "fallback response"
    assert response.provider == "gemini"
    assert response.fallback_used is True
    assert openrouter.calls == 1
    assert gemini.calls == 1
    assert groq.calls == 0
