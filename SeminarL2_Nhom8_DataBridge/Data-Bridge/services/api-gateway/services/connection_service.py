"""Connection service logic."""

import logging
import psycopg2
from typing import Any, Optional

from core.connection_store import connection_store
from core.encryption import encrypt_value, decrypt_value
from schemas.connection_schemas import ConnectionCreateRequest

logger = logging.getLogger(__name__)

class ConnectionService:
    """Business logic for database connections."""

    def create(self, owner_id: str, request: ConnectionCreateRequest):
        """Create a new connection after encrypting the password."""
        try:
            params = request.model_dump()
            # Encrypt password
            params["password_enc"] = encrypt_value(params.pop("password"))
            
            # Save to DB
            return connection_store.create_connection(owner_id, params)
        except Exception as e:
            logger.error(f"Failed to create connection: {e}")
            raise

    def update(self, connection_id: str, owner_id: str, request: Any):
        """Update an existing connection."""
        try:
            params = {k: v for k, v in request.model_dump().items() if v is not None}
            if "password" in params:
                params["password_enc"] = encrypt_value(params.pop("password"))
            
            return connection_store.update_connection(connection_id, owner_id, params)
        except Exception as e:
            logger.error(f"Failed to update connection {connection_id}: {e}")
            raise

    def list(self, user_id: str):
        """List all connections for a user."""
        return connection_store.list_connections(user_id)

    def delete(self, connection_id: str, owner_id: str):
        """Delete a connection."""
        return connection_store.delete_connection(connection_id, owner_id)

    def test_connection(self, connection_id: str, user_id: str):
        """Test a connection by attempting to connect to the target DB."""
        conn_info = connection_store.get_connection(connection_id, user_id)
        if not conn_info:
            return {"success": False, "error": "Connection not found or access denied"}

        try:
            # Decrypt password
            password = decrypt_value(conn_info["password_enc"])
            
            db_type = conn_info.get("db_type", "postgresql")
            
            if db_type == "mongodb":
                import pymongo
                import urllib.parse
                
                # Always construct the URI dynamically to ensure we use the decrypted password securely
                enc_user = urllib.parse.quote_plus(conn_info["username"])
                enc_pass = urllib.parse.quote_plus(password)
                
                # Use mongodb+srv for Atlas domains
                is_srv = "mongodb.net" in conn_info['host']
                protocol = "mongodb+srv" if is_srv else "mongodb"
                
                uri = f"{protocol}://{enc_user}:{enc_pass}@{conn_info['host']}"
                
                # SRV records don't need ports, standard mongodb does
                if not is_srv and conn_info.get('port'):
                    uri += f":{conn_info['port']}"
                
                # Append database name
                db_name = conn_info.get('database_name', '')
                if db_name and db_name != 'default':
                    uri += f"/{db_name}"
                else:
                    uri += "/"
                    db_name = "admin" # fallback for ping
                
                # For Atlas, authSource=admin is highly recommended
                uri += "?retryWrites=true&w=majority&authSource=admin"
                
                # Test connection using pymongo
                client = pymongo.MongoClient(uri, serverSelectionTimeoutMS=5000)
                client.admin.command('ping')
                client.close()
                return {"success": True, "database": db_name}
            
            else:
                # Default PostgreSQL connection
                target_conn = psycopg2.connect(
                    host=conn_info["host"],
                    port=conn_info["port"],
                    dbname=conn_info["database_name"],
                    user=conn_info["username"],
                    password=password,
                    connect_timeout=5
                )
                
                # Simple query to verify
                with target_conn.cursor() as cur:
                    cur.execute("SELECT current_database()")
                    db_name = cur.fetchone()[0]
                    
                target_conn.close()
                return {"success": True, "database": db_name}
                
        except Exception as e:
            error_str = str(e)
            logger.warning(f"Connection test failed for {connection_id}: {error_str}")
            
            # Make MongoDB auth errors more user-friendly
            if "bad auth" in error_str.lower() or "authentication failed" in error_str.lower():
                friendly_error = (
                    "Authentication failed: Incorrect username or password. "
                    "If using MongoDB Atlas, ensure your 'Database User' is fully created, "
                    "the password matches exactly, and it has finished deploying."
                )
                return {"success": False, "error": friendly_error}
                
            return {"success": False, "error": error_str}

    def add_member(self, connection_id: str, admin_id: str, target_email: str, role: str):
        """Add a member to a connection using their email."""
        return connection_store.add_member(connection_id, admin_id, target_email, role)

    def get_members(self, connection_id: str, admin_id: str):
        """Get list of members for a connection."""
        return connection_store.get_members(connection_id, admin_id)
        
    def remove_member(self, connection_id: str, admin_id: str, target_email: str):
        """Remove a member from a connection using their email."""
        return connection_store.remove_member(connection_id, admin_id, target_email)

connection_service = ConnectionService()
