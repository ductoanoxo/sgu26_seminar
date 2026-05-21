from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ColumnDef:
    name: str
    type: str


@dataclass
class SourceMeta:
    name: str
    columns: List[ColumnDef] = field(default_factory=list)
    estimated_rows: Optional[int] = None


class BaseAdapter(ABC):
    @abstractmethod
    def test_connection(self) -> bool: ...

    @abstractmethod
    def list_sources(self) -> List[SourceMeta]: ...

    @abstractmethod
    def read_data(self, source: str, limit: int = 10000) -> Dict[str, Any]:
        """Returns {'columns': [str], 'rows': [dict]}"""
        ...

    @abstractmethod
    def close(self): ...
