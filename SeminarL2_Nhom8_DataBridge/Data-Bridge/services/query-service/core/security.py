"""SQL security validation layer.

Provides multi-layer validation to ensure only safe SELECT queries are executed.
"""

import re
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Dangerous SQL keywords that must be rejected
FORBIDDEN_KEYWORDS = [
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bALTER\b",
    r"\bCREATE\b",
    r"\bTRUNCATE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b",
    r"\bMERGE\b",
    r"\bCALL\b",
    r"\bCOPY\b",
    r"\bLOAD\b",
    r"\bREPLACE\b",
    r"\bUPSERT\b",
]

# Dangerous patterns
DANGEROUS_PATTERNS = [
    r";\s*\w",               # Multiple statements (semicolon followed by another statement)
    r"--",                   # SQL comments (potential injection)
    r"/\*",                  # Block comments
    r"xp_\w+",              # Extended stored procedures
    r"sp_\w+",              # System stored procedures
    r"\bINTO\s+OUTFILE\b",  # File writing
    r"\bINTO\s+DUMPFILE\b", # File writing
    r"\bLOAD_FILE\b",       # File reading
    r"\bUTL_FILE\b",        # Oracle file access
    r"\bDBMS_\w+",          # Oracle packages
    r"\bpg_sleep\b",        # PostgreSQL sleep
    r"\bbenchmark\b",       # MySQL benchmark
    r"\bwaitfor\b",         # SQL Server wait
]


@dataclass
class ValidationResult:
    """Result of SQL validation."""
    is_valid: bool
    error_message: str | None = None
    sanitized_sql: str | None = None


def validate_sql(sql: str) -> ValidationResult:
    """
    Validate that a SQL query is safe to execute.

    Performs multi-layer validation:
    1. Empty/whitespace check
    2. SELECT-only enforcement
    3. Forbidden keyword detection
    4. Dangerous pattern detection
    5. Query sanitization

    Args:
        sql: The SQL query to validate.

    Returns:
        ValidationResult with validation status and details.
    """
    if not sql or not sql.strip():
        return ValidationResult(
            is_valid=False,
            error_message="Empty SQL query provided."
        )

    # Normalize the SQL: remove comments and leading/trailing whitespace
    # Strip single line comments
    normalized = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
    # Strip block comments
    normalized = re.sub(r'/\*.*?\*/', '', normalized, flags=re.DOTALL)
    normalized = normalized.strip()

    # Remove trailing semicolons for cleaner processing
    if normalized.endswith(";"):
        normalized = normalized[:-1].strip()

    # Layer 1: Must start with SELECT or WITH (for CTEs)
    upper_sql = normalized.upper()
    if not (upper_sql.startswith("SELECT") or upper_sql.startswith("WITH")):
        return ValidationResult(
            is_valid=False,
            error_message="Only SELECT queries are allowed. Query must start with SELECT or WITH."
        )

    # Layer 2: Check for forbidden keywords
    for pattern in FORBIDDEN_KEYWORDS:
        # Check in the non-string parts of the query
        # Simple approach: check the whole query but account for string literals
        clean_sql = _remove_string_literals(upper_sql)
        if re.search(pattern, clean_sql, re.IGNORECASE):
            keyword = re.search(pattern, clean_sql, re.IGNORECASE).group()
            return ValidationResult(
                is_valid=False,
                error_message=f"Forbidden SQL keyword detected: {keyword}. Only SELECT queries are allowed."
            )

    # Layer 3: Check for dangerous patterns
    clean_sql = _remove_string_literals(normalized)
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, clean_sql, re.IGNORECASE):
            return ValidationResult(
                is_valid=False,
                error_message=f"Potentially dangerous SQL pattern detected. Query rejected for security."
            )

    # Layer 4: Check for multiple statements
    clean_sql = _remove_string_literals(normalized)
    if ";" in clean_sql:
        return ValidationResult(
            is_valid=False,
            error_message="Multiple SQL statements are not allowed."
        )

    logger.info(f"SQL validation passed: {normalized[:100]}...")
    return ValidationResult(
        is_valid=True,
        sanitized_sql=normalized
    )


def _remove_string_literals(sql: str) -> str:
    """Remove string literals from SQL to avoid false positives in keyword detection."""
    # Remove single-quoted strings
    result = re.sub(r"'[^']*'", "''", sql)
    # Remove double-quoted identifiers
    result = re.sub(r'"[^"]*"', '""', result)
    return result
