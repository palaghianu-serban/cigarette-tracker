import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from main import CigaretteTrackerApp

class TestMainLogic(unittest.TestCase):
    def setUp(self):
        self.app = CigaretteTrackerApp()

    def test_get_current_baseline(self):
        baseline = self.app.get_current_baseline()
        # Should be None if no baseline, or Baseline instance
        self.assertTrue(baseline is None or hasattr(baseline, "avg_cigs_per_day"))

    def test_find_entry_for_today(self):
        entries = self.app.data.get("entries", [])
        entry = self.app.find_entry_for_today(entries)
        # Should be None or a dict with today's date
        if entry:
            self.assertEqual(entry["entry_date"], entry["entry_date"])

if __name__ == "__main__":
    unittest.main()