"""Architect Agent — Analyzes user intent and selects relevant tables."""

import logging
from core.llm_client import BaseLLMClient
from core.prompts import ARCHITECT_AGENT_PROMPT, DATABASE_SCHEMA
from domain.models import ArchitectOutput

logger = logging.getLogger(__name__)


class ArchitectAgent:
    """Analyzes user intent and determines which tables are needed."""

    def __init__(self, llm_client: BaseLLMClient):
        self._llm = llm_client

    def run(self, user_query: str) -> ArchitectOutput:
        """Analyze the user query and return architecture plan."""
        logger.info(f"[ArchitectAgent] Analyzing: '{user_query}'")

        prompt = ARCHITECT_AGENT_PROMPT.format(
            schema=DATABASE_SCHEMA,
            user_query=user_query,
        )

        try:
            result = self._llm.generate_json(prompt, temperature=0.1)
            output = ArchitectOutput(
                intent=result.get("intent", ""),
                selected_tables=result.get("selected_tables", []),
                join_needed=result.get("join_needed", False),
                join_hints=result.get("join_hints", ""),
                aggregation=result.get("aggregation", "none"),
                filters=result.get("filters", ""),
                sorting=result.get("sorting", ""),
                limit=result.get("limit"),
                query_plan=result.get("query_plan", ""),
            )
            logger.info(f"[ArchitectAgent] Selected tables: {output.selected_tables}")
            logger.info(f"[ArchitectAgent] Intent: {output.intent}")
            return output
        except Exception as e:
            logger.error(f"[ArchitectAgent] Failed: {e}")
            raise
