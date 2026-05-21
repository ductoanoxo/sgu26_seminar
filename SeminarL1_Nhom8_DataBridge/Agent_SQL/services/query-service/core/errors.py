"""Query service error mapping utilities."""

import psycopg2

SQLSTATE_MESSAGES = {
    "42601": "Query syntax error. Please check your SQL.",
    "42P01": "Table not found. Please check table names.",
    "42703": "Column not found. Please check selected fields.",
    "57014": "Query timed out. Please narrow the result set.",
}

DEFAULT_ERROR_MESSAGE = "Query execution failed. Please check your SQL and try again."


def map_query_error(exc: Exception) -> str:
    if isinstance(exc, psycopg2.Error):
        code = getattr(exc, "pgcode", None)
        if code and code in SQLSTATE_MESSAGES:
            return SQLSTATE_MESSAGES[code]
        return "Query execution failed. Please verify your SQL syntax and table names."
    return DEFAULT_ERROR_MESSAGE
