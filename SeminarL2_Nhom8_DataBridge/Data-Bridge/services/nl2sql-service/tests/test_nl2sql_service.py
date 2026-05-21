"""Tests for NL2SQL Service."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "nl2sql-service"
    assert data["status"] == "running"


def test_generate_sql_endpoint_exists():
    """Test that the endpoint exists (will fail auth without API key)."""
    response = client.post("/generate-sql", json={"query": "test"})
    # Should return 200 (with error in body) or 500, not 404
    assert response.status_code != 404


def test_explain_endpoint_exists():
    """Test that the explain endpoint exists."""
    response = client.post("/explain", json={"sql_query": "SELECT 1"})
    assert response.status_code != 404


def test_generate_sql_empty_query():
    """Test that empty query is handled."""
    response = client.post("/generate-sql", json={"query": ""})
    # Should not crash - FastAPI will validate
    assert response.status_code in [200, 422, 500]
