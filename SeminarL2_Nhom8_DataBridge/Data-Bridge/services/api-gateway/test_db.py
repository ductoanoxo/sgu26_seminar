import os
from dotenv import load_dotenv
import psycopg2
import json

load_dotenv()
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()
cur.execute("SELECT name, db_type, host, settings FROM app_private.connections ORDER BY created_at DESC LIMIT 3;")
for row in cur.fetchall():
    print(row)
