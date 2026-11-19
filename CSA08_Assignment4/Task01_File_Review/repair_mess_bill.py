"""Safer hostel mess-bill processing: streaming, validation and audit trail."""
from decimal import Decimal, InvalidOperation
from pathlib import Path

def total_mess_bills(filename):
    report, rejected = [], []
    total = Decimal("0.00")
    with open(filename, "r", encoding="utf-8") as file:
        for line_no, raw in enumerate(file, start=1):
            if not raw.strip():       # Ignore blank lines, including a trailing line.
                continue
            parts = [part.strip() for part in raw.rstrip("\\n").split(",")]
            try:
                if len(parts) != 3:
                    raise ValueError(f"expected 3 fields, found {len(parts)}")
                reg, name, amount_text = parts
                if not reg or not name:
                    raise ValueError("register number and name are required")
                amount = Decimal(amount_text)
                if not amount.is_finite() or amount < 0:
                    raise ValueError("amount must be finite and non-negative")
            except (ValueError, InvalidOperation) as error:
                rejected.append((line_no, raw.rstrip(), str(error)))
                continue
            total += amount
            report.append(f"{name}: {amount:.2f}")
    return report, total, rejected

def main():
    sample = Path(__file__).with_name("mess_oct_sample.txt")
    report, total, rejected = total_mess_bills(sample)
    print("TASK 1 - REPAIRED MESS BILL REPORT")
    print("\\n".join(report))
    print(f"Total: {total:.2f}")
    print("Rejected records:")
    for line_no, line, reason in rejected:
        print(f"Line {line_no}: {line!r} ({reason})")

if __name__ == "__main__":
    main()
