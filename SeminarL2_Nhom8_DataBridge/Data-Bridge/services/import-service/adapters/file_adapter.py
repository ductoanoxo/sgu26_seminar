import io
import json
import pandas as pd
from typing import List, Dict, Any
from .base import ColumnDef, SourceMeta
from .sql_adapter import SQLFileAdapter


def _safe_col(name: str) -> str:
    return str(name).strip().replace(" ", "_").replace("-", "_").replace(".", "_")


class FileAdapter:
    """Parse CSV, Excel (.xlsx/.xls), JSON, Parquet, SQL dump files into DataFrames."""

    def __init__(self, file_content: bytes, filename: str):
        self._filename = filename.lower()
        self._df_map: Dict[str, pd.DataFrame] = {}
        self._sql_adapter: SQLFileAdapter | None = None
        self._parse(file_content)

    def _parse(self, content: bytes):
        if self._filename.endswith(".sql"):
            self._sql_adapter = SQLFileAdapter(content, self._filename)
            return

        if self._filename.endswith(".parquet"):
            import pyarrow.parquet as pq
            table = pq.read_table(io.BytesIO(content))
            df = table.to_pandas()
            df.columns = [_safe_col(c) for c in df.columns]
            name = self._filename.removesuffix(".parquet").replace("-", "_").replace(" ", "_")
            self._df_map[name] = df

        elif self._filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
            df.columns = [_safe_col(c) for c in df.columns]
            name = self._filename.removesuffix(".csv").replace("-", "_").replace(" ", "_")
            self._df_map[name] = df

        elif self._filename.endswith((".xlsx", ".xls")):
            xl = pd.ExcelFile(io.BytesIO(content))
            for sheet in xl.sheet_names:
                df = xl.parse(sheet)
                df.columns = [_safe_col(c) for c in df.columns]
                safe_name = sheet.replace("-", "_").replace(" ", "_").lower()
                self._df_map[safe_name] = df

        elif self._filename.endswith(".json"):
            data = json.loads(content)
            if isinstance(data, list):
                df = pd.DataFrame(data)
                df.columns = [_safe_col(c) for c in df.columns]
                name = self._filename.removesuffix(".json").replace("-", "_").replace(" ", "_")
                self._df_map[name] = df
            elif isinstance(data, dict):
                for key, val in data.items():
                    if isinstance(val, list):
                        df = pd.DataFrame(val)
                        df.columns = [_safe_col(c) for c in df.columns]
                        self._df_map[key] = df

    def list_sources(self) -> List[SourceMeta]:
        if self._sql_adapter is not None:
            return self._sql_adapter.list_sources()
        result = []
        for name, df in self._df_map.items():
            cols = [ColumnDef(name=c, type=str(df[c].dtype)) for c in df.columns]
            result.append(SourceMeta(name=name, columns=cols, estimated_rows=len(df)))
        return result

    def read_data(self, source: str, limit: int = 10000) -> Dict[str, Any]:
        if self._sql_adapter is not None:
            return self._sql_adapter.read_data(source, limit)
        df = self._df_map.get(source)
        if df is None:
            return {"columns": [], "rows": []}
        df = df.head(limit).where(pd.notna(df), None)
        return {
            "columns": list(df.columns),
            "rows": df.to_dict(orient="records"),
        }
