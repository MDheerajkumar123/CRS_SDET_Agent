TASK_PROVIDER_MAP = {
    "crs_analyzer": "gemini",
    "requirement_reviewer": "openrouter",
    "risk_strategy": "openrouter",
    "scenario": "groq",
    "test_design": "openrouter",
    "test_case_validator": "openrouter",
    "test_case": "gemini",
    "rtm": "groq",
    "final_reviewer": "openrouter",
    "scenario_validator": "openrouter",
    "rtm_validator": "openrouter",
}


FALLBACK_PROVIDER_MAP = {
    "gemini": ["openrouter", "groq"],
    "openrouter": ["gemini", "groq"],
    "groq": ["openrouter", "gemini"],
}


def get_provider_for_task(task_name: str) -> str:
    """
    Return the primary provider assigned to a task.
    """

    if task_name not in TASK_PROVIDER_MAP:
        raise ValueError(
            f"Unknown task: {task_name}"
        )

    return TASK_PROVIDER_MAP[task_name]


def get_fallback_provider(provider_name: str) -> list[str]:
    """
    Return the ordered fallback providers.
    """

    if provider_name not in FALLBACK_PROVIDER_MAP:
        raise ValueError(
            f"No fallback configured for provider: {provider_name}"
        )

    return FALLBACK_PROVIDER_MAP[provider_name]
