import json
from datetime import datetime
import os

# Get the parent directory of the scripts folder
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_DIR, "smoking_data.json")

def add_created_at():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for baseline in data.get("baselines", []):
        if "created_at" not in baseline:
            baseline["created_at"] = now

    for entry in data.get("entries", []):
        if "created_at" not in entry:
            entry["created_at"] = now

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    add_created_at()
    print("All baselines and entries updated with created_at.")