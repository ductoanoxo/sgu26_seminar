"""Tests for dashboard storage normalization."""

import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.dashboard_store import _normalize_row


def test_normalize_row_serializes_timestamp_fields():
    created_at = datetime(2026, 5, 16, 10, 30, tzinfo=timezone.utc)
    updated_at = datetime(2026, 5, 16, 11, 45, tzinfo=timezone.utc)

    row = _normalize_row(
        {
            "id": "dashboard-1",
            "name": "Sales",
            "owner_id": "user-1",
            "widgets": [],
            "created_at": created_at,
            "updated_at": updated_at,
        }
    )

    assert row["created_at"] == created_at.isoformat()
    assert row["updated_at"] == updated_at.isoformat()
