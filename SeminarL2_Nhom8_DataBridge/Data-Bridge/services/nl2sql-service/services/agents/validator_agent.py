"""Validator Agent — Validates generated SQL for safety and correctness."""

import logging
from core.llm_client import BaseLLMClient
from core.prompts import VALIDATOR_AGENT_PROMPT
from core.schema_cache import get_schema
from domain.models import ValidatorOutput

logger = logging.getLogger(__name__)


class ValidatorAgent:
    """Validates SQL queries for safety, correctness, and quality."""

    def __init__(self, llm_client: BaseLLMClient):
        self._llm = llm_client
        self.prompt_template = VALIDATOR_AGENT_PROMPT
        self.schema = get_schema()

    def run(self, user_query: str, sql_query: str, explanation: str, schema: str | None = None) -> ValidatorOutput:
        """Validate the generated SQL query."""
        logger.info(f"[ValidatorAgent] Validating SQL: {sql_query[:100]}...")

        prompt = VALIDATOR_AGENT_PROMPT.format(
            schema=schema or get_schema(),
            user_query=user_query,
            sql_query=sql_query,
            explanation=explanation,
        )

        try:
            result = self._llm.generate_json(prompt, temperature=0.1)
            safety = result.get("safety_check", {})
            corrected_sql = result.get("corrected_sql", sql_query)
            
            # Ensure string format
            if isinstance(corrected_sql, (dict, list)):
                corrected_sql = json.dumps(corrected_sql)
                
            output = ValidatorOutput(
                is_valid=result.get("is_valid", False),
                is_safe=result.get("is_safe", False),
                issues=result.get("issues", []),
                suggestions=result.get("suggestions", []),
                corrected_sql=corrected_sql,
                corrected_explanation=result.get("corrected_explanation", explanation),
                safety_check=safety,
            )
            logger.info(f"[ValidatorAgent] Valid: {output.is_valid}, Safe: {output.is_safe}")
            if output.issues:
                logger.warning(f"[ValidatorAgent] Issues: {output.issues}")
            return output
        except Exception as e:
            logger.error(f"[ValidatorAgent] Failed: {e}")
            raise
