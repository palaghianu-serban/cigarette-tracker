import json
import os
from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_DIR, "smoking_data.json")

def align_json_with_db():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Baseline columns
    baseline_keys = ["avg_cigs_per_day", "pack_size", "pack_price", "created_at"]
    # Entry columns
    entry_keys = [
        "entry_date",
        "cigs_smoked",
        "money_saved",
        "productive_minutes_saved",
        "source",
        "created_at"
    ]

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Align baselines
    for baseline in data.get("baselines", []):
        for key in baseline_keys:
            if key not in baseline:
                if key == "created_at":
                    baseline[key] = now_str
                else:
                    baseline[key] = 0.0 if key == "pack_price" else 0

    # Align entries
    for entry in data.get("entries", []):
        for key in entry_keys:
            if key not in entry:
                if key == "created_at":
                    entry[key] = now_str
                elif key == "source":
                    entry[key] = "manual"
                elif key in ["money_saved", "productive_minutes_saved"]:
                    entry[key] = 0.0 if key == "money_saved" else 0
                elif key == "cigs_smoked":
                    entry[key] = 0
                else:
                    entry[key] = ""

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("JSON data aligned with database columns.")

if __name__ == "__main__":
    align_json_with_db()