from app.llm.crewai_llm import _OpenRouterJSONLLM


def test_openrouter_structured_call_uses_configured_completion_path(monkeypatch):
    captured = {}

    def fake_call(self, **kwargs):
        captured.update(kwargs)
        return '{"result": "normal completion"}'

    monkeypatch.setattr("app.llm.crewai_llm.OpenAICompletion.call", fake_call)
    llm = _OpenRouterJSONLLM(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        provider="openai",
        api_key="test-key",
        base_url="https://openrouter.ai/api/v1",
        custom_openai=True,
    )

    response = llm.call(
        [{"role": "user", "content": "Return JSON."}],
        response_model=object,
    )

    assert response == '{"result": "normal completion"}'
    assert captured["response_model"] is None
