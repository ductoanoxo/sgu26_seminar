"""Query history logging."""

import json
import os
import logging
from datetime import datetime, timezone
from core.config import get_settings

logger = logging.getLogger(__name__)


class HistoryManager:
    """File-based query history logging."""

    def __init__(self):
        self._settings = get_settings()
        self._file = self._settings.HISTORY_FILE

    def log_query(
        self,
        question: str,
        sql: str,
        explanation: str,
        success: bool,
        row_count: int = 0,
        source: str = "ai",
        sql_original: str | None = None,
        duration_ms: int = 0,
    ):
        history = self._load()
        entry = {
            "id": len(history) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question": question,
            "sql_query": sql,
            "sql_original": sql_original,
            "explanation": explanation,
            "success": success,
            "row_count": row_count,
            "duration_ms": duration_ms,
            "source": source,
        }
        history.append(entry)
        self._save(history)
        return entry

    def get_history(self, limit: int = 20) -> list[dict]:
        history = self._load()
        return list(reversed(history[-limit:]))

    def _load(self) -> list[dict]:
        if not os.path.exists(self._file):
            return []
        try:
            with open(self._file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def _save(self, history: list[dict]):
        try:
            with open(self._file, "w") as f:
                json.dump(history, f, indent=2, default=str)
        except IOError as e:
            logger.error(f"Failed to save history: {e}")


history_manager = HistoryManager()
