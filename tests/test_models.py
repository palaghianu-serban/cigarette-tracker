import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from models import Baseline, DailyEntry
from datetime import date

class TestModels(unittest.TestCase):
    def test_baseline_creation(self):
        b = Baseline(20, 20, 30.0, "2025-09-08 21:18:17")
        self.assertEqual(b.avg_cigs_per_day, 20)
        self.assertEqual(b.pack_size, 20)
        self.assertEqual(b.pack_price, 30.0)
        self.assertEqual(b.created_at, "2025-09-08 21:18:17")

    def test_daily_entry_creation(self):
        e = DailyEntry(date.today().isoformat(), 10, 5.0, 50, "manual", "2025-09-08 21:18:17")
        self.assertEqual(e.entry_date, date.today().isoformat())
        self.assertEqual(e.cigs_smoked, 10)
        self.assertEqual(e.money_saved, 5.0)
        self.assertEqual(e.productive_minutes_saved, 50)
        self.assertEqual(e.source, "manual")
        self.assertEqual(e.created_at, "2025-09-08 21:18:17")

if __name__ == "__main__":
    unittest.main()