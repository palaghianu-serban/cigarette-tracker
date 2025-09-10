import json

JSON_PATH = "smoking_data.json"

def add_source_to_entries():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data.get("entries", []):
        entry["source"] = "manual"

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    add_source_to_entries()
    print("All entries updated with source='manual'.")