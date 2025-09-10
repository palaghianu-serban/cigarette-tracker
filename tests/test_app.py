import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from storage import write_json, read_json, migrate_json_to_db, load_data, init_db
from models import Baseline, DailyEntry
from datetime import date

class TestValidation(unittest.TestCase):
    def test_baseline_validation(self):
        b = Baseline(20, 20, 30.0, "2025-09-08 21:18:17")
        self.assertTrue(b.avg_cigs_per_day > 0)
        self.assertTrue(b.pack_size > 0)
        self.assertTrue(b.pack_price > 0)

        b = Baseline(-1, 0, -5.0, "2025-09-08 21:18:17")
        self.assertFalse(b.avg_cigs_per_day > 0)
        self.assertFalse(b.pack_size > 0)
        self.assertFalse(b.pack_price > 0)

    def test_entry_validation(self):
        e = DailyEntry(date.today().isoformat(), 10, 5.0, 50, "manual", "2025-09-08 21:18:17")
        self.assertTrue(e.cigs_smoked >= 0)
        self.assertTrue(e.money_saved >= 0)
        self.assertTrue(e.productive_minutes_saved >= 0)
        self.assertIn(e.source, ["manual", "system"])

        e = DailyEntry(date.today().isoformat(), -5, -1.0, -10, "manual", "2025-09-08 21:18:17")
        self.assertFalse(e.cigs_smoked >= 0)
        self.assertFalse(e.money_saved >= 0)
        self.assertFalse(e.productive_minutes_saved >= 0)

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

    def test_load_data(self):
        data = load_data()
        self.assertTrue(len(data["baselines"]) > 0)
        self.assertTrue(len(data["entries"]) > 0)
        self.assertEqual(data["baselines"][0]["avg_cigs_per_day"], 15)
        self.assertEqual(data["entries"][0]["cigs_smoked"], 10)

    def tearDown(self):
        write_json({"baselines": [], "entries": []})
        migrate_json_to_db()

if __name__ == "__main__":
    unittest.main()