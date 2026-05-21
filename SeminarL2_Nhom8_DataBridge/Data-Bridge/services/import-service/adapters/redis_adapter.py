"""Redis adapter — exports keys grouped by data type as virtual tables."""

import redis
from typing import List, Dict, Any, Optional
from .base import BaseAdapter, ColumnDef, SourceMeta

# Virtual table names per Redis data type
_TYPE_TABLES = {
    "string":   "redis_strings",
    "hash":     "redis_hashes",
    "list":     "redis_lists",
    "set":      "redis_sets",
    "zset":     "redis_sorted_sets",
}

_TABLE_SCHEMAS: Dict[str, List[ColumnDef]] = {
    "redis_strings":     [ColumnDef("key", "TEXT"), ColumnDef("value", "TEXT")],
    "redis_hashes":      [ColumnDef("key", "TEXT"), ColumnDef("field", "TEXT"), ColumnDef("value", "TEXT")],
    "redis_lists":       [ColumnDef("key", "TEXT"), ColumnDef("index", "INTEGER"), ColumnDef("value", "TEXT")],
    "redis_sets":        [ColumnDef("key", "TEXT"), ColumnDef("member", "TEXT")],
    "redis_sorted_sets": [ColumnDef("key", "TEXT"), ColumnDef("member", "TEXT"), ColumnDef("score", "FLOAT")],
}

_SCAN_BATCH = 200  # keys per SCAN call


class RedisAdapter(BaseAdapter):
    def __init__(
        self,
        host: str,
        port: int,
        database: str,           # used as db index (0-15), defaults to 0
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        db_index = int(database) if database and database.isdigit() else 0
        self._client = redis.Redis(
            host=host,
            port=port or 6379,
            db=db_index,
            username=username or None,
            password=password or None,
            socket_connect_timeout=5,
            decode_responses=True,
        )

    def test_connection(self) -> bool:
        try:
            self._client.ping()
            return True
        except Exception:
            return False

    def list_sources(self) -> List[SourceMeta]:
        """Scan all keys, count per type, return virtual tables."""
        type_counts: Dict[str, int] = {t: 0 for t in _TYPE_TABLES.values()}

        cursor = 0
        while True:
            cursor, keys = self._client.scan(cursor=cursor, count=_SCAN_BATCH)
            for key in keys:
                try:
                    ktype = self._client.type(key)
                    table = _TYPE_TABLES.get(ktype)
                    if table:
                        type_counts[table] += 1
                except Exception:
                    continue
            if cursor == 0:
                break

        result = []
        for table, count in type_counts.items():
            if count > 0:
                result.append(SourceMeta(
                    name=table,
                    columns=_TABLE_SCHEMAS[table],
                    estimated_rows=count,
                ))
        return result

    def read_data(self, source: str, limit: int = 10000) -> Dict[str, Any]:
        """Read all keys of the given type and flatten into rows."""
        reverse_map = {v: k for k, v in _TYPE_TABLES.items()}
        target_type = reverse_map.get(source)
        if not target_type:
            return {"columns": [], "rows": []}

        cols = [c.name for c in _TABLE_SCHEMAS[source]]
        rows: List[Dict] = []

        cursor = 0
        while len(rows) < limit:
            cursor, keys = self._client.scan(cursor=cursor, count=_SCAN_BATCH)
            for key in keys:
                if len(rows) >= limit:
                    break
                try:
                    ktype = self._client.type(key)
                    if ktype != target_type:
                        continue
                    rows.extend(self._read_key(key, ktype, limit - len(rows)))
                except Exception:
                    continue
            if cursor == 0:
                break

        return {"columns": cols, "rows": rows}

    def _read_key(self, key: str, ktype: str, remaining: int) -> List[Dict]:
        rows: List[Dict] = []
        try:
            if ktype == "string":
                val = self._client.get(key)
                rows.append({"key": key, "value": str(val)})

            elif ktype == "hash":
                fields = self._client.hgetall(key)
                for field, val in list(fields.items())[:remaining]:
                    rows.append({"key": key, "field": field, "value": str(val)})

            elif ktype == "list":
                items = self._client.lrange(key, 0, remaining - 1)
                for i, val in enumerate(items):
                    rows.append({"key": key, "index": i, "value": str(val)})

            elif ktype == "set":
                members = self._client.smembers(key)
                for member in list(members)[:remaining]:
                    rows.append({"key": key, "member": str(member)})

            elif ktype == "zset":
                items = self._client.zrange(key, 0, remaining - 1, withscores=True)
                for member, score in items:
                    rows.append({"key": key, "member": str(member), "score": score})
        except Exception:
            pass
        return rows

    def close(self):
        self._client.close()
