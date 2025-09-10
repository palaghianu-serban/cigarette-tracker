import json
import os
from datetime import date, timedelta

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_DIR, "smoking_data.json")

def restore_manual_data():
    # Baseline values
    baseline = {
        "avg_cigs_per_day": 25,
        "pack_size": 20,
        "pack_price": 29.5,
        "created_at": date.today().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Entry for yesterday
    yesterday = date.today() - timedelta(days=1)
    entry_yesterday = {
        "entry_date": yesterday.isoformat(),
        "cigs_smoked": 25,
        "money_saved": 0.0,
        "productive_minutes_saved": 0,
        "source": "manual",
        "created_at": yesterday.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Entry for today
    today = date.today()
    entry_today = {
        "entry_date": today.isoformat(),
        "cigs_smoked": 20,
        "money_saved": 0.0,
        "productive_minutes_saved": 0,
        "source": "manual",
        "created_at": today.strftime("%Y-%m-%d %H:%M:%S")
    }

    data = {
        "baselines": [baseline],
        "entries": [entry_yesterday, entry_today]
    }

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Restored baseline and entries to smoking_data.json.")

if __name__ == "__main__":
    restore_manual_data()