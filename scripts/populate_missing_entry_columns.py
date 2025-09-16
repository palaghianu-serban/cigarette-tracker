import sqlite3

DB_PATH = "smoking_data.db"

def get_latest_baseline(conn):
    c = conn.cursor()
    c.execute("SELECT avg_cigs_per_day, pack_size, pack_price FROM baselines ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    if row:
        return {
            "avg_cigs_per_day": row[0],
            "pack_size": row[1],
            "pack_price": row[2]
        }
    return None

def populate_missing_columns():
    conn = sqlite3.connect(DB_PATH)
    baseline = get_latest_baseline(conn)
    if not baseline:
        print("No baseline found. Cannot populate values.")
        conn.close()
        return

    c = conn.cursor()
    c.execute("SELECT id, cigs_smoked FROM entries")
    entries = c.fetchall()

    for entry_id, cigs_smoked in entries:
        money_spent = (cigs_smoked / baseline["pack_size"]) * baseline["pack_price"]
        productive_minutes_wasted = cigs_smoked * 5
        c.execute(
            "UPDATE entries SET money_spent = ?, productive_minutes_wasted = ? WHERE id = ?",
            (round(money_spent, 2), productive_minutes_wasted, entry_id)
        )

    conn.commit()
    conn.close()
    print("All missing columns populated.")

if __name__ == "__main__":
    populate_missing_columns()