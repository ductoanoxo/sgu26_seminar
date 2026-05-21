"""Tests for API Gateway."""

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
    assert data["service"] == "api-gateway"
    assert data["status"] == "running"


def test_ask_endpoint_exists():
    """Test that the /ask endpoint exists."""
    response = client.post("/ask", json={"question": "test"})
    # Won't succeed without downstream services, but shouldn't be 404
    assert response.status_code != 404


def test_explain_endpoint_exists():
    """Test that /explain endpoint exists."""
    response = client.post("/explain", json={"sql_query": "SELECT 1"})
    assert response.status_code != 404


def test_history_endpoint():
    """Test that /history endpoint exists."""
    response = client.get("/history")
    assert response.status_code == 200


def test_speech_transcribe_endpoint_exists():
    response = client.post(
        "/speech/transcribe",
        data={"model": "not-a-model"},
        files={"file": ("speech.webm", b"audio", "audio/webm")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert "Unsupported model" in data["error"]


def test_ask_validation():
    """Test request validation."""
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_dashboards_list_endpoint_exists():
    response = client.get("/dashboards")
    assert response.status_code != 404


def test_dashboards_create_endpoint_exists():
    response = client.post("/dashboards", json={"name": "Test Dashboard", "widgets": []})
    assert response.status_code != 404


def test_dashboards_refresh_endpoint_exists():
    response = client.post(
        "/dashboards/00000000-0000-0000-0000-000000000000/refresh",
        json={"widget_ids": []},
    )
    assert response.status_code != 404
