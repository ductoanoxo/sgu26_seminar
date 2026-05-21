"""API Gateway domain models."""

from dataclasses import dataclass, field


@dataclass
class GatewayResult:
    success: bool = False
    sql_query: str = ""
    explanation: str = ""
    data: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    error: str | None = None
