import os
from dotenv import load_dotenv

# ✅ Absolute path to .env file
dotenv_path = r"D:\Projects\Nutrilingo\.env"

# ✅ Check if file exists before loading
if os.path.exists(dotenv_path):
    print(f"📄 .env file found at: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path)
else:
    print("❌ .env file not found at the specified path!")

# ✅ Debug print to check value
db_url = os.getenv("DATABASE_URL")
print("Loaded DB URL:", db_url)

from db.db_connect import get_db_connection

conn = get_db_connection()
if conn:
    cursor = conn.cursor()
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()
    print("✅ Connected to the database.")
    print("📋 Tables in DB:", tables)
    conn.close()
else:
    print("❌ Could not connect to DB.")
