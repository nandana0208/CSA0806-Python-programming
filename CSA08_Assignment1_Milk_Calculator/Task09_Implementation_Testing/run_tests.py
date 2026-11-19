from decimal import Decimal
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from calculator import make_entry
from common.milkrate import rate_per_litre, payout, ten_day_total

def run():
    cases = [
        ("standard", "10", "3.5", "8.5", "Morning", "300.00"),
        ("fat+snf above", "8.5", "4.2", "8.7", "Evening", "283.90"),
        ("fat+snf below", "12", "3.1", "8.3", "Morning", "333.60"),
        ("minimum fat", "1", "2.0", "8.5", "Morning", "24.00"),
        ("maximum fat", "1", "7.0", "8.5", "Evening", "44.00"),
    ]
    print("CASE                 EXPECTED    ACTUAL      RESULT")
    results = []
    for name, litres, fat, snf, shift, expected in cases:
        entry = make_entry("FTEST", litres, fat, snf, shift)
        actual = str(payout(entry["litres"], entry["fat"], entry["snf"]))
        ok = actual == expected
        results.append(ok)
        print(f"{name:20} {expected:>8} {actual:>10}  {'PASS' if ok else 'FAIL'}")
    invalid = [
        ("negative litres", ("F", "-1", "3.5", "8.5", "Morning")),
        ("fat below range", ("F", "1", "1.9", "8.5", "Morning")),
        ("fat above range", ("F", "1", "7.1", "8.5", "Morning")),
        ("invalid text", ("F", "eight", "3.5", "8.5", "Morning")),
    ]
    for name, args in invalid:
        try:
            make_entry(*args)
            results.append(False)
            print(name, "FAIL (accepted)")
        except Exception:
            results.append(True)
            print(name, "PASS (rejected)")
    five = [
        make_entry("F1", "10", "3.5", "8.5", "Morning"),
        make_entry("F1", "8.5", "4.2", "8.7", "Evening"),
        make_entry("F2", "12", "3.1", "8.3", "Morning"),
        make_entry("F3", "1", "2.0", "8.5", "Morning"),
        make_entry("F4", "1", "7.0", "8.5", "Evening"),
    ]
    total = ten_day_total(five)
    print("Five-entry total:", total, "expected 985.50")
    results.append(total == Decimal("985.50"))
    assert all(results), "One or more tests failed"
    print(f"All {len(results)} checks passed.")

if __name__ == "__main__":
    run()
