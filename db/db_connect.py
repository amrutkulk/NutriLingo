import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        print("✅ Connected to the database.")
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None
print("Loaded DB URL:", os.getenv("DATABASE_URL"))
