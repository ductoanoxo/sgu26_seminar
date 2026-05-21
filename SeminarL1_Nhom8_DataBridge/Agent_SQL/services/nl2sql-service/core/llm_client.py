"""LLM client abstraction supporting Google Gemini and OpenAI.

Provides a unified interface for LLM calls across the multi-agent pipeline.
"""

import json
import logging
from abc import ABC, abstractmethod

from core.config import get_settings

logger = logging.getLogger(__name__)


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""

    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.1) -> str:
        """Generate a response from the LLM."""
        pass

    def generate_json(self, prompt: str, temperature: float = 0.1) -> dict:
        """Generate a JSON response from the LLM, with fallback parsing."""
        raw = self.generate(prompt, temperature)
        return self._parse_json(raw)

    @staticmethod
    def _parse_json(text: str) -> dict:
        """Parse JSON from LLM output, handling common formatting issues."""
        cleaned = text.strip()

        # Remove markdown code fences if present
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from LLM output: {e}")
            logger.error(f"Raw output: {text[:500]}")
            # Attempt to find JSON in the response
            start = cleaned.find("{")
            end = cleaned.rfind("}") + 1
            if start != -1 and end > start:
                try:
                    return json.loads(cleaned[start:end])
                except json.JSONDecodeError:
                    pass
            raise ValueError(f"Could not parse JSON from LLM response: {text[:200]}")


class GeminiClient(BaseLLMClient):
    """Google Gemini API client."""

    def __init__(self):
        settings = get_settings()
        import google.generativeai as genai

        genai.configure(api_key=settings.GEMINI_API_KEY)
        self._model = genai.GenerativeModel(settings.GEMINI_MODEL)
        logger.info(f"Initialized Gemini client with model: {settings.GEMINI_MODEL}")

    def generate(self, prompt: str, temperature: float = 0.1) -> str:
        import google.generativeai as genai

        response = self._model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            ),
        )
        return response.text


class OpenAIClient(BaseLLMClient):
    """OpenAI API client."""

    def __init__(self):
        settings = get_settings()
        from openai import OpenAI

        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self._model = settings.OPENAI_MODEL
        logger.info(f"Initialized OpenAI client with model: {self._model}")

    def generate(self, prompt: str, temperature: float = 0.1) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise SQL assistant. Always respond with valid JSON when asked. Ensure all strings are properly escaped.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=4096,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content


class OpenRouterClient(BaseLLMClient):
    """OpenRouter API client."""

    def __init__(self):
        settings = get_settings()
        from openai import OpenAI

        self._client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
        )
        self._model = settings.OPENROUTER_MODEL
        logger.info(f"Initialized OpenRouter client with model: {self._model}")

    def generate(self, prompt: str, temperature: float = 0.1) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a precise SQL assistant. Always respond with valid JSON when asked. Ensure all strings are properly escaped.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
            max_tokens=4096,
            response_format={"type": "json_object"},
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-OpenRouter-Title": "NL2SQL Dashboard",
            }
        )
        return response.choices[0].message.content


def create_llm_client() -> BaseLLMClient:
    """Factory function to create the appropriate LLM client."""
    settings = get_settings()
    if settings.LLM_PROVIDER == "gemini":
        return GeminiClient()
    elif settings.LLM_PROVIDER == "openai":
        return OpenAIClient()
    elif settings.LLM_PROVIDER == "openrouter":
        return OpenRouterClient()
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
