from decimal import Decimal
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.milkrate import rate_per_litre, payout, ten_day_total

if __name__ == "__main__":
    sample_entries = [
        {"litres": Decimal("10"), "fat": Decimal("3.5"), "snf": Decimal("8.5")},
        {"litres": Decimal("8.5"), "fat": Decimal("4.2"), "snf": Decimal("8.7")},
    ]
    for entry in sample_entries:
        print("rate", rate_per_litre(entry["fat"], entry["snf"]),
              "payment", payout(entry["litres"], entry["fat"], entry["snf"]))
    print("ten-day total", ten_day_total(sample_entries))
