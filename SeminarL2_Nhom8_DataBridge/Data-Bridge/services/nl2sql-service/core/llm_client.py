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
        
        # If the output is from CoordinatorClient, it's a JSON string with 'result_text'
        try:
            data = json.loads(raw)
            if isinstance(data, dict) and "result_text" in data and "provider" in data:
                # Extract the actual LLM response text from the coordinator's metadata object
                raw = data["result_text"]
        except (json.JSONDecodeError, TypeError):
            # Not a coordinator JSON object, use raw string as is
            pass
            
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
            return json.loads(cleaned, strict=False)
        except json.JSONDecodeError as e:
            repaired = BaseLLMClient._escape_control_chars_in_strings(cleaned)
            if repaired != cleaned:
                try:
                    return json.loads(repaired)
                except json.JSONDecodeError:
                    pass
            logger.error(f"Failed to parse JSON from LLM output: {e}")
            logger.error(f"Raw output (full): {text}")
            
            # Attempt to find JSON in the response
            start = cleaned.find("{")
            end = cleaned.rfind("}") + 1
            if start != -1 and end > start:
                try:
                    candidate = cleaned[start:end]
                    return json.loads(BaseLLMClient._escape_control_chars_in_strings(candidate))
                except json.JSONDecodeError:
                    # Try to fix truncated JSON by adding a closing brace
                    try:
                        return json.loads(cleaned[start:] + '"}', strict=False)
                    except:
                        pass
            raise ValueError(f"Could not parse JSON from LLM response (check logs for full output). Error: {e}")

    @staticmethod
    def _escape_control_chars_in_strings(text: str) -> str:
        """Escape literal newlines/tabs inside JSON strings from loose LLM output."""
        out = []
        in_string = False
        escaped = False
        for ch in text:
            if in_string:
                if escaped:
                    out.append(ch)
                    escaped = False
                elif ch == "\\":
                    out.append(ch)
                    escaped = True
                elif ch == '"':
                    out.append(ch)
                    in_string = False
                elif ch == "\n":
                    out.append("\\n")
                elif ch == "\r":
                    out.append("\\r")
                elif ch == "\t":
                    out.append("\\t")
                else:
                    out.append(ch)
            else:
                out.append(ch)
                if ch == '"':
                    in_string = True
        return "".join(out)


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
                max_output_tokens=2048,
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


class CoordinatorClient(BaseLLMClient):
    """LLM client that routes between Gemini models, rotates keys, and falls back to OpenAI."""

    def __init__(self):
        self.settings = get_settings()
        self.models = self.settings.GEMINI_MODELS
        self.keys = self.settings.GEMINI_KEYS or []
        if self.settings.GEMINI_API_KEY and self.settings.GEMINI_API_KEY not in self.keys:
            self.keys.append(self.settings.GEMINI_API_KEY)

        self.fast_pass_count = self.settings.FAST_PASS_KEY_COUNT
        self.timeout_ms = self.settings.GEMINI_TIMEOUT_MS
        self.cooldown_s = self.settings.GEMINI_COOLDOWN_S
        
        self.active_key_index = 0
        self.last_model_used = None
        self.cooldowns = {}  # key_index -> unban_time

    def _is_retryable(self, error_msg: str, status_code: int = None) -> bool:
        if status_code in (429, 503, 500, 502, 504):
            return True
        error_lower = error_msg.lower()
        for kw in ["timeout", "connection", "resource exhausted", "temporarily unavailable", "internal error"]:
            if kw in error_lower:
                return True
        return False

    def generate(self, prompt: str, temperature: float = 0.1) -> str:
        import time
        import httpx

        attempts = []
        start_time = time.time()
        
        # 1. Try Gemini rotation
        if self.keys and self.models:
            for model_idx, model in enumerate(self.models):
                is_primary = (model_idx == 0)
                
                # Order keys: fast pass first N keys starting from active, then the rest
                ordered_keys = []
                n_keys = len(self.keys)
                for i in range(n_keys):
                    idx = (self.active_key_index + i) % n_keys
                    ordered_keys.append(idx)
                
                # We attempt keys
                for i, k_idx in enumerate(ordered_keys):
                    if time.time() < self.cooldowns.get(k_idx, 0):
                        logger.debug(f"Skipping key {k_idx} due to cooldown.")
                        continue
                    
                    key = self.keys[k_idx]
                    key_snippet = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"
                    
                    attempt_start = time.time()
                    try:
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
                        headers = {"Content-Type": "application/json"}
                        data = {
                            "contents": [{"parts": [{"text": prompt}]}],
                            "generationConfig": {
                                "temperature": temperature,
                                "response_mime_type": "application/json",
                            }
                        }
                        
                        logger.info(f"Attempting Gemini request: model={model}, key_index={k_idx}")
                        
                        with httpx.Client(timeout=self.timeout_ms / 1000.0) as client:
                            response = client.post(url, headers=headers, json=data)
                        
                        elapsed_ms = int((time.time() - attempt_start) * 1000)
                        
                        if response.status_code == 200:
                            res_json = response.json()
                            candidates = res_json.get("candidates", [])
                            if not candidates:
                                raise ValueError(f"Gemini returned no candidates: {res_json}")
                                
                            first_candidate = candidates[0]
                            content = first_candidate.get("content", {})
                            parts = content.get("parts", [])
                            if not parts:
                                raise ValueError(f"Gemini returned no parts: {res_json}")
                                
                            text = parts[0].get("text", "")
                            
                            self.last_model_used = model
                            self.active_key_index = k_idx
                            
                            logger.info(f"Gemini request successful: model={model}, key_index={k_idx}, elapsed={elapsed_ms}ms")
                            
                            attempts.append({
                                "provider": "gemini",
                                "model": model,
                                "key_index": k_idx,
                                "key_snippet": key_snippet,
                                "status": "ok",
                                "elapsed_ms": elapsed_ms,
                                "error_message": None
                            })
                            
                            result_obj = {
                                "result_text": text,
                                "provider": "gemini",
                                "model": model,
                                "last_model_used": self.last_model_used,
                                "key_index": k_idx,
                                "key_snippet": key_snippet,
                                "fallback_used": not is_primary,
                                "error": None,
                                "attempts": attempts,
                                "timing_ms": int((time.time() - start_time) * 1000)
                            }
                            return json.dumps(result_obj)
                            
                        else:
                            error_text = response.text
                            status = response.status_code
                            logger.warning(f"Gemini request failed: model={model}, status={status}, error={error_text}")
                            
                            if self._is_retryable(error_text, status):
                                self.cooldowns[k_idx] = time.time() + self.cooldown_s
                                attempts.append({
                                    "provider": "gemini", "model": model, "key_index": k_idx,
                                    "key_snippet": key_snippet, "status": "retryable_error",
                                    "elapsed_ms": elapsed_ms, "error_message": f"HTTP {status}: {error_text[:100]}"
                                })
                            else:
                                attempts.append({
                                    "provider": "gemini", "model": model, "key_index": k_idx,
                                    "key_snippet": key_snippet, "status": "permanent_error",
                                    "elapsed_ms": elapsed_ms, "error_message": f"HTTP {status}: {error_text[:100]}"
                                })
                                # Skip this model+key on permanent error
                                continue
                                
                    except Exception as e:
                        elapsed_ms = int((time.time() - attempt_start) * 1000)
                        logger.error(f"Gemini attempt exception: {str(e)}")
                        self.cooldowns[k_idx] = time.time() + self.cooldown_s
                        attempts.append({
                            "provider": "gemini", "model": model, "key_index": k_idx,
                            "key_snippet": key_snippet, "status": "retryable_error",
                            "elapsed_ms": elapsed_ms, "error_message": str(e)
                        })

        # 2. Fallback to OpenAI / OpenRouter
        attempt_start = time.time()
        try:
            from openai import OpenAI
            
            # Determine which fallback to use
            if self.settings.OPENAI_API_KEY and self.settings.OPENAI_API_KEY != "your-openai-api-key":
                api_key = self.settings.OPENAI_API_KEY
                base_url = self.settings.OPENAI_BASE_URL
                model_name = self.settings.OPENAI_MODEL
                provider_name = "openai"
                extra_headers = None
            else:
                api_key = self.settings.OPENROUTER_API_KEY
                base_url = "https://openrouter.ai/api/v1"
                model_name = self.settings.OPENROUTER_MODEL
                provider_name = "openrouter"
                extra_headers = {
                    "HTTP-Referer": "http://localhost:3000",
                    "X-OpenRouter-Title": "NL2SQL Dashboard",
                }

            client = OpenAI(
                base_url=base_url,
                api_key=api_key
            )
            
            kwargs = {
                "model": model_name,
                "messages": [
                    {
                        "role": "system",
                        "content": "Return only one valid compact JSON object. Do not use markdown.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature
            }
            if provider_name in {"openai", "openrouter"}:
                kwargs["response_format"] = {"type": "json_object"}
            if extra_headers:
                kwargs["extra_headers"] = extra_headers

            response = client.chat.completions.create(**kwargs)
            text = response.choices[0].message.content
            elapsed_ms = int((time.time() - attempt_start) * 1000)
            
            attempts.append({
                "provider": provider_name, "model": model_name, "key_index": None,
                "key_snippet": None, "status": "ok", "elapsed_ms": elapsed_ms,
                "error_message": None
            })
            
            result_obj = {
                "result_text": text,
                "provider": provider_name,
                "model": model_name,
                "last_model_used": model_name,
                "key_index": None,
                "key_snippet": None,
                "fallback_used": True,
                "error": None,
                "attempts": attempts,
                "timing_ms": int((time.time() - start_time) * 1000)
            }
            return json.dumps(result_obj)
            
        except Exception as e:
            elapsed_ms = int((time.time() - attempt_start) * 1000)
            
            # Re-evaluate provider and model in case exception happened before assignments
            p_name = "openai" if (self.settings.OPENAI_API_KEY and self.settings.OPENAI_API_KEY != "your-openai-api-key") else "openrouter"
            m_name = self.settings.OPENAI_MODEL if p_name == "openai" else self.settings.OPENROUTER_MODEL
            
            attempts.append({
                "provider": p_name, "model": m_name, "key_index": None,
                "key_snippet": None, "status": "permanent_error", "elapsed_ms": elapsed_ms,
                "error_message": str(e)
            })
            
            result_obj = {
                "result_text": f"Error: All LLM attempts failed. Last error: {attempts[-1]['error_message'] if attempts else 'No attempts made'}",
                "provider": "none",
                "model": "none",
                "last_model_used": self.last_model_used,
                "key_index": None,
                "key_snippet": None,
                "fallback_used": True,
                "error": "All models and fallbacks failed.",
                "attempts": attempts,
                "timing_ms": int((time.time() - start_time) * 1000)
            }
            return json.dumps(result_obj)


def create_llm_client() -> BaseLLMClient:
    """Factory function to create the appropriate LLM client."""
    settings = get_settings()
    if settings.LLM_PROVIDER == "gemini":
        return GeminiClient()
    elif settings.LLM_PROVIDER == "openai":
        return OpenAIClient()
    elif settings.LLM_PROVIDER == "openrouter":
        return OpenRouterClient()
    elif settings.LLM_PROVIDER == "coordinator":
        return CoordinatorClient()
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
