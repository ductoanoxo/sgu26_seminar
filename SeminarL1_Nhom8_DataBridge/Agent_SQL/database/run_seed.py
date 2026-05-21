import psycopg2
import os
from dotenv import load_dotenv

# Load env from query-service
load_dotenv("/home/traductoan/Seminar_Final/services/query-service/.env")

def seed_database():
    host = os.getenv("SUPABASE_DB_HOST")
    port = os.getenv("SUPABASE_DB_PORT")
    dbname = os.getenv("SUPABASE_DB_NAME")
    user = os.getenv("SUPABASE_DB_USER")
    password = os.getenv("SUPABASE_DB_PASSWORD")

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

        print("Reading seed.sql...")
        with open("/home/traductoan/Seminar_Final/database/seed.sql", "r") as f:
            seed_sql = f.read()

        print("Executing seed script...")
        # psycopg2 can execute multiple statements separated by semicolons
        cur.execute(seed_sql)
        
        print("Database seeded successfully!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error seeding database: {e}")

if __name__ == "__main__":
    seed_database()
