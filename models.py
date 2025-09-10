from dataclasses import dataclass
from datetime import date

@dataclass
class Baseline:
    avg_cigs_per_day: int
    pack_size: int
    pack_price: float
    created_at: str = ""  # Add this line

@dataclass
class DailyEntry:
    entry_date: str  # Use str if you store ISO date strings
    cigs_smoked: int
    money_saved: float
    productive_minutes_saved: int
    source: str
    created_at: str = ""  # Add this line