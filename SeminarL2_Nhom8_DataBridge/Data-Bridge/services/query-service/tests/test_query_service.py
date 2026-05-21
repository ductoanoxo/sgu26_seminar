"""Tests for Query Service."""

import os
import sys
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from core.errors import map_query_error
from core.security import validate_sql


# ─── SQL Validation Tests ───


def test_valid_select():
    result = validate_sql("SELECT * FROM users")
    assert result.is_valid is True


def test_valid_select_with_where():
    result = validate_sql("SELECT name, email FROM users WHERE country = 'USA'")
    assert result.is_valid is True


def test_valid_select_with_join():
    sql = "SELECT u.name, o.total_amount FROM users u JOIN orders o ON u.id = o.user_id"
    result = validate_sql(sql)
    assert result.is_valid is True


def test_valid_cte():
    sql = "WITH totals AS (SELECT user_id, SUM(total_amount) AS total FROM orders GROUP BY user_id) SELECT * FROM totals"
    result = validate_sql(sql)
    assert result.is_valid is True


def test_reject_insert():
    result = validate_sql("INSERT INTO users (name) VALUES ('hacker')")
    assert result.is_valid is False
    assert "SELECT" in result.error_message  # Rejected by SELECT-only check


def test_reject_update():
    result = validate_sql("UPDATE users SET name = 'hacked' WHERE id = 1")
    assert result.is_valid is False


def test_reject_delete():
    result = validate_sql("DELETE FROM users WHERE id = 1")
    assert result.is_valid is False


def test_reject_drop():
    result = validate_sql("DROP TABLE users")
    assert result.is_valid is False


def test_reject_alter():
    result = validate_sql("ALTER TABLE users ADD COLUMN hacked BOOLEAN")
    assert result.is_valid is False


def test_reject_multiple_statements():
    result = validate_sql("SELECT * FROM users; DROP TABLE users")
    assert result.is_valid is False


def test_reject_empty():
    result = validate_sql("")
    assert result.is_valid is False


def test_reject_sql_comment_injection():
    result = validate_sql("SELECT * FROM users -- WHERE admin = true")
    assert result.is_valid is False


def test_api_health():
    from main import app
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "query-service"


class FakePsycopgError(psycopg2.Error):
    def __init__(self, pgcode: str | None):
        super().__init__("database error")
        self.pgcode = pgcode


def test_map_query_error_default_message():
    message = map_query_error(RuntimeError("boom"))
    assert "Query execution failed" in message


def test_map_query_error_sqlstate_message():
    message = map_query_error(FakePsycopgError("42601"))
    assert "syntax" in message.lower()


def test_map_query_error_unknown_sqlstate():
    message = map_query_error(FakePsycopgError("99999"))
    assert "verify your sql" in message.lower()
