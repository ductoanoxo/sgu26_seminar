"""Query service domain models."""

from dataclasses import dataclass, field


@dataclass
class QueryResult:
    columns: list[str] = field(default_factory=list)
    rows: list[dict] = field(default_factory=list)
    row_count: int = 0
    duration_ms: int = 0
    truncated: bool = False
    success: bool = True
    error: str | None = None
