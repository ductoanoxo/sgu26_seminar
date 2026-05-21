from pymongo import MongoClient
from typing import List, Dict, Any, Optional
from urllib.parse import quote, unquote
from .base import BaseAdapter, ColumnDef, SourceMeta


def _normalize_uri(uri: str) -> str:
    """Auto-encode special characters in username/password of a database URI."""
    proto_end = uri.find('://')
    if proto_end == -1:
        return uri
    scheme = uri[:proto_end]
    rest = uri[proto_end + 3:]

    at_positions = [i for i, c in enumerate(rest) if c == '@']
    if not at_positions:
        return uri

    last_at = at_positions[-1]
    auth = rest[:last_at]
    host_path = rest[last_at + 1:]

    colon_pos = auth.find(':')
    if colon_pos == -1:
        return f"{scheme}://{quote(unquote(auth), safe='')}@{host_path}"

    raw_user = auth[:colon_pos]
    raw_pass = auth[colon_pos + 1:]

    user_encoded = quote(unquote(raw_user), safe='')
    pass_encoded = quote(unquote(raw_pass), safe='')

    return f"{scheme}://{user_encoded}:{pass_encoded}@{host_path}"

_SYSTEM_DBS = {"admin", "local", "config"}


def _flatten_doc(doc: dict, prefix: str = "") -> dict:
    """Flatten nested MongoDB document into single-level dict."""
    result = {}
    for key, value in doc.items():
        if key == "_id":
            result["_id"] = str(value)
            continue
        full_key = f"{prefix}_{key}" if prefix else key
        if isinstance(value, dict):
            result.update(_flatten_doc(value, full_key))
        elif isinstance(value, list):
            result[full_key] = str(value)
        else:
            result[full_key] = value
    return result


class MongoDBAdapter(BaseAdapter):
    def __init__(
        self, host: str = "localhost", port: int = 27017, database: str = "",
        username: Optional[str] = None, password: Optional[str] = None,
        connection_string: Optional[str] = None,
    ):
        if connection_string:
            uri = _normalize_uri(connection_string)
            if not database:
                from urllib.parse import urlparse
                parsed = urlparse(connection_string)
                db_from_path = parsed.path.lstrip("/").split("?")[0]
                database = db_from_path  # may be empty — handled below
        else:
            auth = ""
            if username and password:
                auth = f"{username}:{password}@"
            uri = f"mongodb://{auth}{host}:{port or 27017}/"

        self._client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # If no database specified, we'll scan all databases in list_sources/read_data
        self._database = database or ""

    def _get_db_and_coll(self, source: str):
        """Parse 'dbname.collection' or plain 'collection' using self._database."""
        if "." in source:
            db_name, coll_name = source.split(".", 1)
            return self._client[db_name], coll_name
        return self._client[self._database or "test"], source

    def test_connection(self) -> bool:
        try:
            self._client.server_info()
            return True
        except Exception:
            return False

    def list_sources(self) -> List[SourceMeta]:
        result = []

        if self._database:
            # Specific database — list its collections only
            db = self._client[self._database]
            for name in sorted(db.list_collection_names()):
                result.append(self._collection_meta(db, name, name))
        else:
            # No database specified — scan all non-system databases
            for db_name in sorted(self._client.list_database_names()):
                if db_name in _SYSTEM_DBS:
                    continue
                db = self._client[db_name]
                for coll_name in sorted(db.list_collection_names()):
                    source_name = f"{db_name}.{coll_name}"
                    result.append(self._collection_meta(db, coll_name, source_name))

        return result

    def _collection_meta(self, db, coll_name: str, source_name: str) -> SourceMeta:
        sample = db[coll_name].find_one()
        cols: List[ColumnDef] = []
        if sample:
            flat = _flatten_doc(sample)
            for k, v in flat.items():
                cols.append(ColumnDef(name=k, type=type(v).__name__))
        row_count = db[coll_name].estimated_document_count()
        return SourceMeta(name=source_name, columns=cols, estimated_rows=row_count)

    def read_data(self, source: str, limit: int = 10000) -> Dict[str, Any]:
        db, coll_name = self._get_db_and_coll(source)
        docs = list(db[coll_name].find().limit(limit))
        if not docs:
            return {"columns": [], "rows": []}

        flat_docs = [_flatten_doc(doc) for doc in docs]

        seen: set = set()
        all_keys: List[str] = []
        for doc in flat_docs:
            for k in doc.keys():
                if k not in seen:
                    all_keys.append(k)
                    seen.add(k)

        rows = [{k: doc.get(k) for k in all_keys} for doc in flat_docs]
        return {"columns": all_keys, "rows": rows}

    def close(self):
        self._client.close()
