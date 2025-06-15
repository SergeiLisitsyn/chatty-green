import psycopg2
import os
import sys

def check_postgres():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PG_NAME", "chattydb_v1"),
            user=os.getenv("PG_USER", "chattydb_v1_user"),
            password=os.getenv("PG_PASSWORD", 'cd4gpaNSyycyHFqJrXXTdqfeg7pZQeg'),
            host=os.getenv("DB_HOST", "dpg-d0vutevdiees73f95v70-a"),
            port=os.getenv("DB_PORT", "5432"),
        )
        conn.close()
        print("✅ Successfully connected to the database.")
    except Exception as e:
        print(f"❌ Failed to connect to the database: {e}")
        sys.exit(1)