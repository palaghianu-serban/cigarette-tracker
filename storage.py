import json
import sqlite3
import shutil
import os
from datetime import datetime
from scripts.cleanup_old_backups import cleanup_old_backups

DB_PATH = "smoking_data.db"
JSON_PATH = "smoking_data.json"

def write_json(data):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def read_json():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def migrate_json_to_db():
    data = read_json()
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Create tables if not exist
        c.execute("""
            CREATE TABLE IF NOT EXISTS baselines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                avg_cigs_per_day INTEGER,
                pack_size INTEGER,
                pack_price REAL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entry_date TEXT UNIQUE,
                cigs_smoked INTEGER,
                money_saved REAL,
                money_spent REAL,
                productive_minutes_saved INTEGER,
                productive_minutes_wasted INTEGER,
                source TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            )
        """)
        # Add indexes for performance
        c.execute("CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(entry_date)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_baselines_created_at ON baselines(created_at)")
        # Clear tables before migration
        c.execute("DELETE FROM baselines")
        c.execute("DELETE FROM entries")
        # Insert baselines
        for baseline in data.get("baselines", []):
            c.execute(
                "INSERT INTO baselines (avg_cigs_per_day, pack_size, pack_price, created_at) VALUES (?, ?, ?, ?)",
                (
                    baseline.get("avg_cigs_per_day", 0),
                    baseline.get("pack_size", 0),
                    baseline.get("pack_price", 0.0),
                    baseline.get("created_at", baseline.get("created_at", ""))
                )
            )
        # Insert entries, ensure all required fields are present
        for entry in data.get("entries", []):
            entry.setdefault("cigs_smoked", 0)
            entry.setdefault("money_saved", 0)
            entry.setdefault("money_spent", 0)
            entry.setdefault("productive_minutes_saved", 0)
            entry.setdefault("productive_minutes_wasted", 0)
            entry.setdefault("source", "manual")
            entry.setdefault("created_at", entry.get("created_at", entry["entry_date"] + " 00:00:00"))
            c.execute(
                "INSERT OR REPLACE INTO entries (entry_date, cigs_smoked, money_saved, money_spent, productive_minutes_saved, productive_minutes_wasted, source, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    entry["entry_date"],
                    entry["cigs_smoked"],
                    entry["money_saved"],
                    entry["money_spent"],
                    entry["productive_minutes_saved"],
                    entry["productive_minutes_wasted"],
                    entry["source"],
                    entry["created_at"]
                )
            )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Migration error:", e)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS baselines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            avg_cigs_per_day INTEGER NOT NULL,
            pack_size INTEGER NOT NULL,
            pack_price REAL NOT NULL,
            created_at TEXT DEFAULT (datetime('now')) NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TEXT UNIQUE NOT NULL,
            cigs_smoked INTEGER NOT NULL,
            money_saved REAL NOT NULL,
            productive_minutes_saved INTEGER NOT NULL,
            source TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')) NOT NULL
        )
    """)
    # Add indexes for performance
    c.execute("CREATE INDEX IF NOT EXISTS idx_entries_date ON entries(entry_date)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_baselines_created_at ON baselines(created_at)")
    conn.commit()
    conn.close()

def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT avg_cigs_per_day, pack_size, pack_price, created_at FROM baselines ORDER BY id")
        baselines = [dict(zip(["avg_cigs_per_day", "pack_size", "pack_price", "created_at"], row)) for row in c.fetchall()]
        c.execute("SELECT entry_date, cigs_smoked, money_saved, productive_minutes_saved, source, created_at FROM entries ORDER BY entry_date")
        entries = [dict(zip(["entry_date", "cigs_smoked", "money_saved", "productive_minutes_saved", "source", "created_at"], row)) for row in c.fetchall()]
        conn.close()
        return {"baselines": baselines, "entries": entries}
    except Exception as e:
        print("Database error:", e)
        return {"baselines": [], "entries": []}

def vacuum_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("VACUUM;")
        conn.close()
    except Exception as e:
        print("Vacuum error:", e)

def backup_db(backup_path):
    try:
        shutil.copy2(DB_PATH, backup_path)
        print(f"Backup created at {backup_path}")
    except Exception as e:
        print("Backup error:", e)

def restore_db(backup_path):
    try:
        shutil.copy2(backup_path, DB_PATH)
        print(f"Database restored from {backup_path}")
    except Exception as e:
        print("Restore error:", e)

def automated_backup():
    backup_dir = os.path.join(os.path.dirname(DB_PATH), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"smoking_data_backup_{timestamp}.db")
    try:
        shutil.copy2(DB_PATH, backup_path)
        print(f"Backup created at {backup_path}")
        cleanup_old_backups()  # Automatically clean up old backups
    except Exception as e:
        print("Backup error:", e)