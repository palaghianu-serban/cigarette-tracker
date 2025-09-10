import json
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_DIR, "smoking_data.json")

def recalculate_fields():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data["baselines"]:
        print("No baseline found.")
        return

    baseline = data["baselines"][-1]
    avg_cigs = baseline["avg_cigs_per_day"]
    pack_size = baseline["pack_size"]
    pack_price = baseline["pack_price"]

    for entry in data["entries"]:
        cigs = entry["cigs_smoked"]
        cigs_saved = avg_cigs - cigs
        packs_saved = cigs_saved / pack_size
        money_saved = packs_saved * pack_price
        productive_minutes_saved = cigs_saved * 5
        entry["money_saved"] = round(money_saved, 2)
        entry["productive_minutes_saved"] = productive_minutes_saved

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Recalculated money_saved and productive_minutes_saved for all entries.")

if __name__ == "__main__":
    recalculate_fields()