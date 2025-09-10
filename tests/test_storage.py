import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from storage import write_json, read_json, migrate_json_to_db, load_data, init_db, vacuum_db

# Use a separate JSON file for testing
import storage
storage.JSON_PATH = os.path.join(os.path.dirname(__file__), "smoking_data_test.json")

from datetime import date

class TestStorage(unittest.TestCase):
    def setUp(self):
        init_db()
        self.test_data = {
            "baselines": [{
                "avg_cigs_per_day": 15,
                "pack_size": 20,
                "pack_price": 25.0,
                "created_at": "2025-09-08 21:18:17"
            }],
            "entries": [{
                "entry_date": date.today().isoformat(),
                "cigs_smoked": 10,
                "money_saved": 5.0,
                "productive_minutes_saved": 50,
                "source": "manual",
                "created_at": "2025-09-08 21:18:17"
            }]
        }
        write_json(self.test_data)
        migrate_json_to_db()

    def test_json_read_write(self):
        data = read_json()
        self.assertEqual(data["baselines"][0]["avg_cigs_per_day"], 15)
        self.assertEqual(data["entries"][0]["cigs_smoked"], 10)

    def test_db_migration_and_load(self):
        data = load_data()
        self.assertEqual(data["baselines"][0]["avg_cigs_per_day"], 15)
        self.assertEqual(data["entries"][0]["cigs_smoked"], 10)

    def test_vacuum(self):
        try:
            vacuum_db()
        except Exception as e:
            self.fail(f"Vacuum failed: {e}")

    def tearDown(self):
        write_json({"baselines": [], "entries": []})
        migrate_json_to_db()

if __name__ == "__main__":
    unittest.main()