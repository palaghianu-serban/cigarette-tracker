import json
from datetime import datetime

JSON_PATH = "smoking_data.json"

def update_json_entries():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Use the latest baseline for calculations
    baseline = data["baselines"][-1]
    avg_cigs = baseline["avg_cigs_per_day"]
    pack_size = baseline["pack_size"]
    pack_price = baseline["pack_price"]

    for entry in data.get("entries", []):
        cigs = entry.get("cigs_smoked", 0)
        # Calculate missing fields
        entry["money_spent"] = round((cigs / pack_size) * pack_price, 2)
        entry["productive_minutes_wasted"] = cigs * 5
        # Ensure source and created_at are present
        entry["source"] = entry.get("source", "manual")
        entry["created_at"] = entry.get("created_at", f"{entry['entry_date']} 00:00:00")
        # Ensure money_saved and productive_minutes_saved are present
        entry["money_saved"] = entry.get("money_saved", round((avg_cigs - cigs) / pack_size * pack_price, 2))
        entry["productive_minutes_saved"] = entry.get("productive_minutes_saved", (avg_cigs - cigs) * 5)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("JSON entries updated and normalized.")

if __name__ == "__main__":
    update_json_entries()