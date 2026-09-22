import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

GEMINI_MODEL = os.getenv("GEMINI_MODEL")
GROQ_MODEL = os.getenv("GROQ_MODEL")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

PROVIDER_CONFIG = {
    "gemini": {
        "api_key": GEMINI_API_KEY,
        "model": GEMINI_MODEL,
    },
    "groq": {
        "api_key": GROQ_API_KEY,
        "model": GROQ_MODEL,
    },
    "openrouter": {
        "api_key": OPENROUTER_API_KEY,
        "model": OPENROUTER_MODEL,
    },
}

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
MAX_EMPTY_RESPONSE_RETRIES = int(
    os.getenv("MAX_EMPTY_RESPONSE_RETRIES", "1")
)
QUALITY_THRESHOLD = int(os.getenv("QUALITY_THRESHOLD", "85"))
