from google import genai
from groq import Groq
from openai import OpenAI

from .config import PROVIDER_CONFIG


class GeminiProvider:
    def __init__(self):
        api_key = PROVIDER_CONFIG["gemini"]["api_key"]

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt: str, model: str) -> str:
        response = self.client.models.generate_content(
            model=model,
            contents=prompt,
        )

        return response.text


class GroqProvider:
    def __init__(self):
        api_key = PROVIDER_CONFIG["groq"]["api_key"]

        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        self.client = Groq(api_key=api_key)

    def generate(self, prompt: str, model: str) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content


class OpenRouterProvider:
    def __init__(self):
        api_key = PROVIDER_CONFIG["openrouter"]["api_key"]

        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is not configured.")

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    def generate(self, prompt: str, model: str) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content
