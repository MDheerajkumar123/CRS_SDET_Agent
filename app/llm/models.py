from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    provider: str
    model: str
    task: str
    fallback_used: bool = False
