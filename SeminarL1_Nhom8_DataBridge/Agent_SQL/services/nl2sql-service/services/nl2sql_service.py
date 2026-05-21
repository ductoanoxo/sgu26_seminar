"""NL2SQL orchestration service — runs the multi-agent pipeline."""

import json
import logging
from core.llm_client import create_llm_client, BaseLLMClient
from core.prompts import SQL_EXPLAIN_PROMPT, DATABASE_SCHEMA
from services.agents.architect_agent import ArchitectAgent
from services.agents.sql_generator_agent import SQLGeneratorAgent
from services.agents.validator_agent import ValidatorAgent
from domain.models import PipelineResult

logger = logging.getLogger(__name__)


class NL2SQLService:
    """Orchestrates the multi-agent NL2SQL pipeline."""

    def __init__(self):
        self._llm: BaseLLMClient | None = None
        self._architect: ArchitectAgent | None = None
        self._generator: SQLGeneratorAgent | None = None
        self._validator: ValidatorAgent | None = None

    def _ensure_initialized(self):
        """Lazy initialization of LLM client and agents."""
        if self._llm is None:
            self._llm = create_llm_client()
            self._architect = ArchitectAgent(self._llm)
            self._generator = SQLGeneratorAgent(self._llm)
            self._validator = ValidatorAgent(self._llm)
            logger.info("NL2SQL pipeline initialized")

    def generate_sql(self, user_query: str) -> PipelineResult:
        """Run the full multi-agent pipeline to convert NL to SQL."""
        self._ensure_initialized()
        steps = []
        logger.info(f"=== Pipeline Start: '{user_query}' ===")

        try:
            # ── Agent 1: Architect ──
            logger.info("── Step 1: Architect Agent ──")
            architect_output = self._architect.run(user_query)
            steps.append({
                "agent": "Architect Agent",
                "input_summary": f"User query: '{user_query}'",
                "output_summary": f"Intent: {architect_output.intent} | Tables: {architect_output.selected_tables}",
                "raw_output": {
                    "intent": architect_output.intent,
                    "selected_tables": architect_output.selected_tables,
                    "join_needed": architect_output.join_needed,
                    "aggregation": architect_output.aggregation,
                    "query_plan": architect_output.query_plan,
                },
            })

            # ── Agent 2: SQL Generator ──
            logger.info("── Step 2: SQL Generator Agent ──")
            generator_output = self._generator.run(user_query, architect_output)
            steps.append({
                "agent": "SQL Generator Agent",
                "input_summary": f"Query + Architect plan for tables: {architect_output.selected_tables}",
                "output_summary": f"Generated SQL: {generator_output.sql_query[:80]}...",
                "raw_output": {
                    "sql_query": generator_output.sql_query,
                    "explanation": generator_output.explanation,
                },
            })

            # ── Agent 3: Validator ──
            logger.info("── Step 3: Validator Agent ──")
            validator_output = self._validator.run(
                user_query,
                generator_output.sql_query,
                generator_output.explanation,
            )
            steps.append({
                "agent": "Validator Agent",
                "input_summary": f"SQL to validate: {generator_output.sql_query[:80]}...",
                "output_summary": f"Valid: {validator_output.is_valid}, Safe: {validator_output.is_safe}",
                "raw_output": {
                    "is_valid": validator_output.is_valid,
                    "is_safe": validator_output.is_safe,
                    "issues": validator_output.issues,
                    "suggestions": validator_output.suggestions,
                    "safety_check": validator_output.safety_check,
                },
            })

            # ── Check validation result ──
            if not validator_output.is_valid or not validator_output.is_safe:
                issues_str = "; ".join(validator_output.issues) if validator_output.issues else "Unknown"
                logger.warning(f"Pipeline rejected query: {issues_str}")
                return PipelineResult(
                    success=False,
                    error=f"Query validation failed: {issues_str}",
                    intermediate_steps=steps,
                    selected_tables=architect_output.selected_tables,
                )

            # Use corrected SQL if available
            final_sql = validator_output.corrected_sql or generator_output.sql_query
            final_explanation = validator_output.corrected_explanation or generator_output.explanation

            logger.info(f"=== Pipeline Complete ===")
            return PipelineResult(
                success=True,
                sql_query=final_sql,
                explanation=final_explanation,
                selected_tables=architect_output.selected_tables,
                intermediate_steps=steps,
            )

        except Exception as e:
            logger.error(f"Pipeline error: {e}", exc_info=True)
            return PipelineResult(
                success=False,
                error=f"Pipeline execution failed: {str(e)}",
                intermediate_steps=steps,
            )

    def explain_sql(self, sql_query: str) -> str:
        """Explain a SQL query in natural language."""
        self._ensure_initialized()
        prompt = SQL_EXPLAIN_PROMPT.format(
            sql_query=sql_query,
            schema=DATABASE_SCHEMA,
        )
        return self._llm.generate(prompt, temperature=0.3)


nl2sql_service = NL2SQLService()
