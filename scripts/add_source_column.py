import sqlite3

DB_PATH = "smoking_data.db"

def add_source_column():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE entries ADD COLUMN source TEXT")
        print("Column 'source' added to 'entries' table.")
    except sqlite3.OperationalError as e:
        print("Could not add column (it may already exist):", e)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    add_source_column()