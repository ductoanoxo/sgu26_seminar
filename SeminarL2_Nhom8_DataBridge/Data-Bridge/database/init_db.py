import psycopg2
import os
import glob
from dotenv import load_dotenv

# Load env from api-gateway
load_dotenv("/home/traductoan/Seminar_Final/services/api-gateway/.env")

def init_database():
    host = os.getenv("SUPABASE_DB_HOST")
    port = os.getenv("SUPABASE_DB_PORT")
    dbname = os.getenv("SUPABASE_DB_NAME")
    user = os.getenv("SUPABASE_DB_USER")
    password = os.getenv("SUPABASE_DB_PASSWORD")

    if not all([host, port, dbname, user, password]):
        print("Error: Missing database environment variables.")
        return

    print(f"Connecting to {host}...")
    
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Files to apply in order
        schema_files = [
            "connection_schema.sql",
            "dashboard_schema.sql",
            "seed.sql"
        ]

        for filename in schema_files:
            filepath = os.path.join("/home/traductoan/Seminar_Final/database", filename)
            if not os.path.exists(filepath):
                print(f"Warning: File {filepath} not found. Skipping.")
                continue
                
            print(f"Applying {filename}...")
            with open(filepath, "r") as f:
                sql = f.read()
                cur.execute(sql)
                print(f"Successfully applied {filename}.")
        
        print("Database initialization complete!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == "__main__":
    init_database()
