import sqlite3
import os

# Get the parent directory of the scripts folder
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_DIR, "smoking_data.db")

def add_created_at_column():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE baselines ADD COLUMN created_at TEXT")
    except sqlite3.OperationalError as e:
        print("baselines:", e)
    try:
        c.execute("ALTER TABLE entries ADD COLUMN created_at TEXT")
    except sqlite3.OperationalError as e:
        print("entries:", e)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_created_at_column()
    print("created_at columns added (or already exist).")