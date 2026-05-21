"""SQL Generator Agent — Generates SQL from architect analysis."""

import json
import logging
from core.llm_client import BaseLLMClient
from core.prompts import SQL_GENERATOR_AGENT_PROMPT, DATABASE_SCHEMA
from domain.models import ArchitectOutput, GeneratorOutput

logger = logging.getLogger(__name__)


class SQLGeneratorAgent:
    """Generates SQL queries based on architect analysis."""

    def __init__(self, llm_client: BaseLLMClient):
        self._llm = llm_client

    def run(self, user_query: str, architect_output: ArchitectOutput) -> GeneratorOutput:
        """Generate SQL query from architect analysis."""
        logger.info(f"[SQLGeneratorAgent] Generating SQL for: '{user_query}'")

        architect_dict = {
            "intent": architect_output.intent,
            "selected_tables": architect_output.selected_tables,
            "join_needed": architect_output.join_needed,
            "join_hints": architect_output.join_hints,
            "aggregation": architect_output.aggregation,
            "filters": architect_output.filters,
            "sorting": architect_output.sorting,
            "limit": architect_output.limit,
            "query_plan": architect_output.query_plan,
        }

        prompt = SQL_GENERATOR_AGENT_PROMPT.format(
            schema=DATABASE_SCHEMA,
            user_query=user_query,
            architect_output=json.dumps(architect_dict, indent=2),
        )

        try:
            result = self._llm.generate_json(prompt, temperature=0.1)
            output = GeneratorOutput(
                sql_query=result.get("sql_query", ""),
                explanation=result.get("explanation", ""),
            )
            logger.info(f"[SQLGeneratorAgent] Generated SQL: {output.sql_query[:100]}...")
            return output
        except Exception as e:
            logger.error(f"[SQLGeneratorAgent] Failed: {e}")
            raise
