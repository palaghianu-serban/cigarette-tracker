from storage import read_json, write_json
import sqlite3
from datetime import date, timedelta

DB_PATH = "smoking_data.db"
JSON_PATH = "smoking_data.json"

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
                productive_minutes_saved INTEGER,
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
                "INSERT INTO baselines (avg_cigs_per_day, pack_size, pack_price) VALUES (?, ?, ?)",
                (baseline["avg_cigs_per_day"], baseline["pack_size"], baseline["pack_price"])
            )
        # Insert entries, with correct system/manual logic
        today = date.today().isoformat()
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        manual_entries = {e["entry_date"]: e for e in data.get("entries", []) if e.get("source") == "manual"}
        for entry in data.get("entries", []):
            # Only insert system entry for yesterday if missing manual entry
            if entry.get("source") == "system":
                if entry["entry_date"] == today:
                    continue  # Never log system entry for today
                if entry["entry_date"] == yesterday and yesterday in manual_entries:
                    continue  # Don't log system entry for yesterday if manual exists
            c.execute(
                "INSERT OR REPLACE INTO entries (entry_date, cigs_smoked, money_saved, productive_minutes_saved, source) VALUES (?, ?, ?, ?, ?)",
                (
                    entry["entry_date"],
                    entry.get("cigs_smoked", 0),
                    entry.get("money_saved", 0),
                    entry.get("productive_minutes_saved", 0),
                    entry.get("source", "manual")
                )
            )
        conn.commit()
        conn.close()
    except Exception as e:
        print("Migration error:", e)

def auto_populate_missing_days():
    data = read_json()
    # Gather existing entry dates
    existing_dates = set(e["entry_date"] for e in data.get("entries", []))
    if not existing_dates:
        return  # Nothing to do if no entries at all

    first_entry_date = min(existing_dates)
    first_entry = date.fromisoformat(first_entry_date)
    today = date.today()

    # Get latest baseline
    if not data.get("baselines"):
        return  # No baseline, nothing to populate
    baseline = data["baselines"][-1]
    avg_cigs_per_day = baseline["avg_cigs_per_day"]
    pack_size = baseline["pack_size"]
    pack_price = baseline["pack_price"]

    # Populate missing days after first entry
    d = first_entry
    while d <= today:
        d_str = d.isoformat()
        if d_str not in existing_dates:
            # Insert baseline entry for missing day, source = 'system'
            cigs = avg_cigs_per_day
            packs_smoked = cigs / pack_size
            money_spent = packs_smoked * pack_price
            productive_minutes_wasted = cigs * 5
            packs_saved = 0
            money_saved = 0
            productive_minutes_saved = 0
            data["entries"].append({
                "entry_date": d_str,
                "cigs_smoked": cigs,
                "money_saved": money_saved,
                "productive_minutes_saved": productive_minutes_saved,
                "source": "system",
                "created_at": d.strftime("%Y-%m-%d 00:00:00")
            })
        d += timedelta(days=1)
    write_json(data)

if __name__ == "__main__":
    auto_populate_missing_days()
    migrate_json_to_db()
    print("Migration complete and missing days populated!")