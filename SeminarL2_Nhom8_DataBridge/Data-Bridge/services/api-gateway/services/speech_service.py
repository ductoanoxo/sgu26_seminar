"""Speech-to-text service using local Whisper or Groq Whisper models."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import Any

import anyio
from fastapi import UploadFile

from core.config import get_settings


LOCAL_WHISPER_MODELS = {"base", "small"}
GROQ_WHISPER_MODELS = {"whisper-large-v3", "whisper-large-v3-turbo"}
SUPPORTED_STT_MODELS = LOCAL_WHISPER_MODELS | GROQ_WHISPER_MODELS


class SpeechToTextError(Exception):
    """Raised when transcription cannot be completed."""


class SpeechToTextService:
    def __init__(self) -> None:
        self._local_models: dict[str, Any] = {}

    async def transcribe(self, upload: UploadFile, model: str) -> dict[str, Any]:
        model = model.strip()
        if model not in SUPPORTED_STT_MODELS:
            raise SpeechToTextError(
                f"Unsupported model '{model}'. Supported models: {', '.join(sorted(SUPPORTED_STT_MODELS))}"
            )

        temp_path = await self._persist_upload(upload)
        try:
            if model in LOCAL_WHISPER_MODELS:
                return await anyio.to_thread.run_sync(self._transcribe_local, temp_path, model)
            return await anyio.to_thread.run_sync(self._transcribe_groq, temp_path, model)
        finally:
            try:
                os.remove(temp_path)
            except OSError:
                pass

    async def _persist_upload(self, upload: UploadFile) -> str:
        settings = get_settings()
        max_bytes = settings.STT_MAX_FILE_MB * 1024 * 1024
        content = await upload.read()
        if not content:
            raise SpeechToTextError("Audio file is empty.")
        if len(content) > max_bytes:
            raise SpeechToTextError(f"Audio file exceeds {settings.STT_MAX_FILE_MB} MB.")

        suffix = Path(upload.filename or "audio.webm").suffix or ".webm"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(content)
            return temp_file.name

    def _transcribe_local(self, file_path: str, model: str) -> dict[str, Any]:
        try:
            import whisper
        except ImportError as exc:
            raise SpeechToTextError(
                "Local Whisper is not installed. Install the 'openai-whisper' package and ensure ffmpeg is available."
            ) from exc

        if model not in self._local_models:
            self._local_models[model] = whisper.load_model(model)

        result = self._local_models[model].transcribe(file_path)
        return {
            "text": (result.get("text") or "").strip(),
            "provider": "local",
            "model": model,
            "language": result.get("language"),
            "duration": None,
        }

    def _transcribe_groq(self, file_path: str, model: str) -> dict[str, Any]:
        settings = get_settings()
        api_key = settings.GROQ_API_KEY.strip().strip('"').strip("'")
        if not api_key:
            raise SpeechToTextError("GROQ_API_KEY is not configured.")

        try:
            from groq import Groq
        except ImportError as exc:
            raise SpeechToTextError("Groq SDK is not installed. Install the 'groq' package.") from exc

        client = Groq(api_key=api_key)
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(Path(file_path).name, audio_file.read()),
                model=model,
                temperature=0,
                response_format="verbose_json",
            )

        return {
            "text": (getattr(transcription, "text", "") or "").strip(),
            "provider": "groq",
            "model": model,
            "language": getattr(transcription, "language", None),
            "duration": getattr(transcription, "duration", None),
        }


speech_to_text_service = SpeechToTextService()
