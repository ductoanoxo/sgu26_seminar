"""NL2SQL service domain models."""

from dataclasses import dataclass, field


@dataclass
class ArchitectOutput:
    intent: str = ""
    selected_tables: list[str] = field(default_factory=list)
    join_needed: bool = False
    join_hints: str = ""
    aggregation: str = "none"
    filters: str = ""
    sorting: str = ""
    limit: int | None = None
    query_plan: str = ""


@dataclass
class GeneratorOutput:
    sql_query: str = ""
    explanation: str = ""


@dataclass
class ValidatorOutput:
    is_valid: bool = False
    is_safe: bool = False
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    corrected_sql: str = ""
    corrected_explanation: str = ""
    safety_check: dict = field(default_factory=dict)


@dataclass
class PipelineResult:
    success: bool = False
    sql_query: str = ""
    explanation: str = ""
    selected_tables: list[str] = field(default_factory=list)
    intermediate_steps: list[dict] = field(default_factory=list)
    error: str | None = None
