"""Command-line milk payment calculator using Decimal."""
from decimal import Decimal
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.milkrate import validate_entry, rate_per_litre, payout, ten_day_total

def make_entry(farmer_id, litres, fat, snf, shift):
    """Convert raw values to Decimal and validate a collection record."""
    entry = {
        "farmer_id": str(farmer_id).strip(),
        "litres": Decimal(str(litres)),
        "fat": Decimal(str(fat)),
        "snf": Decimal(str(snf)),
        "shift": str(shift).strip().title(),
    }
    validate_entry(entry["farmer_id"], entry["litres"], entry["fat"],
                   entry["snf"], entry["shift"])
    return entry

def format_payment(entry):
    """Return one human-readable payment line."""
    rate = rate_per_litre(entry["fat"], entry["snf"])
    amount = payout(entry["litres"], entry["fat"], entry["snf"])
    return (f'{entry["farmer_id"]:>8} {entry["shift"]:<7} '
            f'{entry["litres"]:>7} L  fat {entry["fat"]:>4}% '
            f'SNF {entry["snf"]:>4}%  rate Rs {rate:>6.2f}  pay Rs {amount:>8.2f}')

def ten_day_farmer_total(entries):
    """Calculate total for one farmer across all collection entries."""
    return ten_day_total(entries)

if __name__ == "__main__":
    examples = [
        make_entry("F001", "10", "3.5", "8.5", "Morning"),
        make_entry("F001", "8.5", "4.2", "8.7", "Evening"),
        make_entry("F002", "12", "3.1", "8.3", "Morning"),
    ]
    for entry in examples:
        print(format_payment(entry))
    print("All-entry total: Rs", ten_day_total(examples))
