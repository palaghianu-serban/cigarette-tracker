import json
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_DIR, "smoking_data.json")

def recalculate_money_saved():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data["baselines"]:
        print("No baseline found.")
        return

    baseline = data["baselines"][-1]
    avg_cigs = baseline["avg_cigs_per_day"]
    pack_size = baseline["pack_size"]
    pack_price = baseline["pack_price"]

    baseline_money_spent = (avg_cigs / pack_size) * pack_price
    baseline_money_spent = round(baseline_money_spent, 2)

    for entry in data["entries"]:
        cigs = entry["cigs_smoked"]
        actual_money_spent = (cigs / pack_size) * pack_price
        actual_money_spent = round(actual_money_spent, 2)
        entry["money_saved"] = round(baseline_money_spent - actual_money_spent, 2)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print("Recalculated money_saved for all entries.")

if __name__ == "__main__":
    recalculate_money_saved()