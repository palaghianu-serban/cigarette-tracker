import sqlite3
import json
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_DIR, "smoking_data.db")
JSON_PATH = os.path.join(PROJECT_DIR, "smoking_data.json")

def restore_json_from_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT avg_cigs_per_day, pack_size, pack_price, created_at FROM baselines ORDER BY id")
    baselines = [
        {
            "avg_cigs_per_day": row[0],
            "pack_size": row[1],
            "pack_price": row[2],
            "created_at": row[3]
        }
        for row in c.fetchall()
    ]
    c.execute("SELECT entry_date, cigs_smoked, money_saved, productive_minutes_saved, source, created_at FROM entries ORDER BY entry_date")
    entries = [
        {
            "entry_date": row[0],
            "cigs_smoked": row[1],
            "money_saved": row[2],
            "productive_minutes_saved": row[3],
            "source": row[4],
            "created_at": row[5]
        }
        for row in c.fetchall()
    ]
    conn.close()

    data = {
        "baselines": baselines,
        "entries": entries
    }
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Restored {len(baselines)} baselines and {len(entries)} entries to smoking_data.json.")

if __name__ == "__main__":
    restore_json_from_db()