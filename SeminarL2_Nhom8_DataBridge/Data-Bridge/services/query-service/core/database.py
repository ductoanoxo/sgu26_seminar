"""Database connection management for Supabase PostgreSQL."""

import psycopg2
import psycopg2.extras
import logging
from contextlib import contextmanager
from typing import Generator, Any

from core.config import get_settings

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages PostgreSQL connections to Supabase."""

    def __init__(self):
        self._settings = get_settings()

    @contextmanager
    def get_connection(self, params: dict | None = None) -> Generator:
        """Get a database connection context manager."""
        conn = None
        try:
            if params:
                # Use dynamic params
                # Build DSN from dict
                dsn = f"host={params['host']} port={params.get('port', 5432)} dbname={params['database_name']} user={params['username']} password={params['password']}"
                conn = psycopg2.connect(dsn)
            else:
                # Use default Supabase connection
                conn = psycopg2.connect(self._settings.database_url)
            
            conn.set_session(readonly=True)
            yield conn
        except psycopg2.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()

    def execute_query(self, sql: str, connection_params: dict | None = None) -> dict[str, Any]:
        """
        Execute a SELECT query and return results as JSON-serializable dict.

        Returns:
            dict with 'columns' and 'rows' keys.
        """
        max_rows = self._settings.QUERY_MAX_ROWS
        timeout_ms = self._settings.QUERY_TIMEOUT_MS

        with self.get_connection(params=connection_params) as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SET LOCAL statement_timeout = %s", (timeout_ms,))
                cur.execute(sql)
                rows = cur.fetchmany(max_rows + 1)
                truncated = len(rows) > max_rows
                if truncated:
                    rows = rows[:max_rows]
                columns = [desc[0] for desc in cur.description] if cur.description else []

                # Convert rows to list of dicts (JSON-serializable)
                serialized_rows = []
                for row in rows:
                    serialized_row = {}
                    for key, value in row.items():
                        # Handle non-serializable types
                        if hasattr(value, "isoformat"):
                            serialized_row[key] = value.isoformat()
                        elif isinstance(value, (int, float, str, bool, type(None))):
                            serialized_row[key] = value
                        else:
                            serialized_row[key] = str(value)
                    serialized_rows.append(serialized_row)

                return {
                    "columns": columns,
                    "rows": serialized_rows,
                    "row_count": len(serialized_rows),
                    "truncated": truncated,
                }

    def test_connection(self) -> bool:
        """Test if the database connection is working."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                    return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    def get_full_schema(self) -> str:
        """Build a markdown schema string from information_schema including imported tables."""
        sql = """
            SELECT t.table_name, c.column_name, c.data_type
            FROM information_schema.tables t
            JOIN information_schema.columns c
                ON t.table_name = c.table_name AND t.table_schema = c.table_schema
            WHERE t.table_schema = 'public'
                AND t.table_type = 'BASE TABLE'
                AND t.table_name NOT IN ('import_registry')
            ORDER BY t.table_name, c.ordinal_position
        """
        conn = None
        try:
            conn = psycopg2.connect(self._settings.database_url)
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
        except Exception as e:
            logger.error(f"get_full_schema failed: {e}")
            return ""
        finally:
            if conn:
                conn.close()

        tables: dict[str, list] = {}
        for table_name, col_name, col_type in rows:
            tables.setdefault(table_name, []).append((col_name, col_type))

        lines = ["## Database Schema (PostgreSQL / Supabase)\n"]
        for table_name, cols in tables.items():
            lines.append(f"\n### Table: {table_name}")
            lines.append("| Column | Type |")
            lines.append("|--------|------|")
            for col_name, col_type in cols:
                lines.append(f"| {col_name} | {col_type} |")

        return "\n".join(lines)

    def get_table_schema(self, table_name: str) -> str:
        """Return a markdown schema string for a single table (used for file data sources)."""
        return self.get_tables_schema([table_name])

    def get_tables_schema(self, table_names: list[str]) -> str:
        """Return a markdown schema string for the selected imported tables only."""
        table_names = [t for t in table_names if t]
        if not table_names:
            return ""
        sql = """
            SELECT t.table_name, c.column_name, c.data_type
            FROM information_schema.tables t
            JOIN information_schema.columns c
                ON t.table_name = c.table_name AND t.table_schema = c.table_schema
            WHERE t.table_schema = 'public'
                AND t.table_type = 'BASE TABLE'
                AND t.table_name = ANY(%s)
            ORDER BY t.table_name, c.ordinal_position
        """
        conn = None
        try:
            conn = psycopg2.connect(self._settings.database_url)
            with conn.cursor() as cur:
                cur.execute(sql, (table_names,))
                rows = cur.fetchall()
        except Exception as e:
            logger.error(f"get_tables_schema failed: {e}")
            return ""
        finally:
            if conn:
                conn.close()

        if not rows:
            return ""

        tables: dict[str, list] = {}
        for table_name, col_name, col_type in rows:
            tables.setdefault(table_name, []).append((col_name, col_type))

        lines = ["## Database Schema (active imported dataset)\n"]
        for table_name, cols in tables.items():
            lines.append(f"\n### Table: {table_name}")
            lines.append("| Column | Type |")
            lines.append("|--------|------|")
            for col_name, col_type in cols:
                lines.append(f"| {col_name} | {col_type} |")

        return "\n".join(lines)


    def get_postgresql_schema(self, connection_params: dict) -> str:
        """Fetch schema directly from PostgreSQL."""
        try:
            with self.get_connection(params=connection_params) as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    # 1. Fetch tables and columns
                    cur.execute("""
                        SELECT 
                            table_name, 
                            column_name, 
                            data_type, 
                            is_nullable 
                        FROM 
                            information_schema.columns 
                        WHERE 
                            table_schema = 'public' 
                        ORDER BY 
                            table_name, ordinal_position;
                    """)
                    columns = cur.fetchall()
                    
                    if not columns:
                        return "## Database Schema (PostgreSQL)\n\n(No tables found in 'public' schema)"
                    
                    # 2. Fetch foreign keys
                    cur.execute("""
                        SELECT
                            tc.table_name, 
                            kcu.column_name, 
                            ccu.table_name AS foreign_table_name,
                            ccu.column_name AS foreign_column_name 
                        FROM 
                            information_schema.table_constraints AS tc 
                            JOIN information_schema.key_column_usage AS kcu
                              ON tc.constraint_name = kcu.constraint_name
                              AND tc.table_schema = kcu.table_schema
                            JOIN information_schema.constraint_column_usage AS ccu
                              ON ccu.constraint_name = tc.constraint_name
                              AND ccu.table_schema = tc.table_schema
                        WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema='public';
                    """)
                    fks = cur.fetchall()
                    
                    # 3. Format as Markdown
                    schema_lines = ["## Database Schema (PostgreSQL Dynamic)\n"]
                    
                    # Group by table
                    tables = {}
                    for col in columns:
                        t_name = col['table_name']
                        if t_name not in tables:
                            tables[t_name] = []
                        tables[t_name].append(col)
                        
                    for t_name, cols in tables.items():
                        schema_lines.append(f"### Table: {t_name}")
                        schema_lines.append("| Column | Type | Nullable |")
                        schema_lines.append("|--------|------|----------|")
                        for c in cols:
                            schema_lines.append(f"| {c['column_name']} | {c['data_type']} | {c['is_nullable']} |")
                        schema_lines.append("")
                        
                    if fks:
                        schema_lines.append("### Relationships")
                        for fk in fks:
                            schema_lines.append(f"- {fk['table_name']}.{fk['column_name']} → {fk['foreign_table_name']}.{fk['foreign_column_name']}")
                        schema_lines.append("")
                        
                    return "\n".join(schema_lines)
        except Exception as e:
            logger.exception("Error fetching PostgreSQL schema")
            return f"## Error fetching PostgreSQL schema: {e}"


    def get_mongodb_schema(self, connection_params: dict) -> str:
        """Fetch schema directly from MongoDB."""
        import pymongo
        import urllib.parse
        
        enc_user = urllib.parse.quote_plus(connection_params["username"])
        enc_pass = urllib.parse.quote_plus(connection_params["password"])
        
        is_srv = "mongodb.net" in connection_params['host']
        protocol = "mongodb+srv" if is_srv else "mongodb"
        uri = f"{protocol}://{enc_user}:{enc_pass}@{connection_params['host']}"
        if not is_srv and connection_params.get('port'):
            uri += f":{connection_params['port']}"
            
        db_name = connection_params.get('database_name')
        if db_name and db_name != 'default':
            uri += f"/{db_name}"
        else:
            db_name = 'test' # Default database for MongoDB
            uri += "/test"
            
        # For Atlas, authSource=admin is common, but the actual data is in db_name
        uri += "?retryWrites=true&w=majority&authSource=admin"

        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        try:
            # Use specified db or default to 'test'
            db = client.get_database(db_name)
            actual_db_name = db.name
            logger.info(f"Fetching schema for MongoDB database: {actual_db_name}")
            
            schema_lines = [f"## Database Schema (MongoDB: {actual_db_name})\n"]
            
            try:
                collections = db.list_collection_names()
            except Exception as e:
                logger.error(f"Failed to list collections in {actual_db_name}: {e}")
                return f"## Error: Could not list collections in database '{actual_db_name}'. Please ensure your user has 'read' permissions on this database. Error: {e}"

            if not collections:
                return f"## Database Schema (MongoDB: {actual_db_name})\n\n(No collections found or access denied)"

            # Filter out system collections
            user_collections = [c for c in collections if not c.startswith("system.")]
            
            schema_lines.append(f"Available Collections: {', '.join(user_collections)}\n")
            
            for coll_name in user_collections:
                schema_lines.append(f"### Collection: {coll_name}")
                schema_lines.append("| Field | Estimated Type |")
                schema_lines.append("|-------|----------------|")
                
                try:
                    # Sample one document to guess types
                    sample = db[coll_name].find_one()
                    if sample:
                        for k, v in sample.items():
                            type_name = type(v).__name__
                            if type_name == 'dict': type_name = 'Object'
                            elif type_name == 'list': type_name = 'Array'
                            elif type_name == 'ObjectId': type_name = 'ObjectId'
                            elif type_name == 'str': type_name = 'String'
                            elif type_name == 'int': type_name = 'Integer'
                            elif type_name == 'float': type_name = 'Double'
                            elif type_name == 'datetime': type_name = 'DateTime'
                            schema_lines.append(f"| {k} | {type_name} |")
                    else:
                        schema_lines.append("| (empty collection) | |")
                except Exception as e:
                    logger.warning(f"Failed to sample collection {coll_name}: {e}")
                    schema_lines.append(f"| (error reading fields) | {e} |")
                    
                schema_lines.append("\n")
                
            return "\n".join(schema_lines)
        except Exception as e:
            logger.exception("Global error fetching MongoDB schema")
            return f"## Error fetching MongoDB schema: {e}"
        finally:
            client.close()

    def execute_mongodb_query(self, query_string: str, connection_params: dict) -> dict:
        """Execute a MongoDB query (Aggregation pipeline) encoded as JSON."""
        import pymongo
        import urllib.parse
        import json
        from bson import json_util
        
        # 1. Parse the MQL JSON payload
        try:
            mql = json.loads(query_string)
            collection_name = mql.get("collection")
            pipeline = mql.get("pipeline", [])
            if not collection_name:
                raise ValueError("MongoDB query JSON must contain a 'collection' field.")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse MongoDB query JSON: {e}")
            raise ValueError(f"Invalid MQL format. Expected JSON. Error: {e}")
            
        # 2. Build URI
        enc_user = urllib.parse.quote_plus(connection_params["username"])
        enc_pass = urllib.parse.quote_plus(connection_params["password"])
        
        is_srv = "mongodb.net" in connection_params['host']
        protocol = "mongodb+srv" if is_srv else "mongodb"
        uri = f"{protocol}://{enc_user}:{enc_pass}@{connection_params['host']}"
        if not is_srv and connection_params.get('port'):
            uri += f":{connection_params['port']}"
            
        db_name = connection_params.get('database_name')
        if db_name and db_name != 'default':
            uri += f"/{db_name}"
        else:
            db_name = 'test'
            uri += "/test"
            
        uri += "?retryWrites=true&w=majority&authSource=admin"

        # 3. Execute
        max_rows = self._settings.QUERY_MAX_ROWS
        client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
        try:
            db = client.get_database(db_name)
            collection = db[collection_name]
            
            # Execute aggregation
            cursor = collection.aggregate(pipeline)
            
            rows = []
            for i, doc in enumerate(cursor):
                if i >= max_rows + 1:
                    break
                rows.append(doc)
                
            truncated = len(rows) > max_rows
            if truncated:
                rows = rows[:max_rows]
                
            # Flatten & serialize rows
            serialized_rows = []
            columns_set = set()
            for row in rows:
                serialized_row = {}
                for k, v in row.items():
                    columns_set.add(k)
                    if hasattr(v, "isoformat"):
                        serialized_row[k] = v.isoformat()
                    elif isinstance(v, (int, float, str, bool, type(None))):
                        serialized_row[k] = v
                    else:
                        # Convert ObjectId, arrays, dicts to string for display
                        serialized_row[k] = json.loads(json_util.dumps(v)) if isinstance(v, (dict, list)) else str(v)
                serialized_rows.append(serialized_row)
                
            return {
                "columns": list(columns_set),
                "rows": serialized_rows,
                "row_count": len(serialized_rows),
                "truncated": truncated,
            }
        finally:
            client.close()

# Singleton instance
db_manager = DatabaseManager()
