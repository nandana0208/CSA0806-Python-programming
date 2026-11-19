"""One-pass monthly attendance processing for daily CSV files."""
from pathlib import Path
from collections import defaultdict
import csv

def process_month(folder, attendance_out, below_out, errors_out):
    counts = defaultdict(lambda: {"P": 0, "A": 0})
    errors = []
    for path in sorted(Path(folder).glob("*.csv")):
        with path.open("r", encoding="utf-8", newline="") as file:
            for line_no, raw in enumerate(file, start=1):
                try:
                    fields = next(csv.reader([raw]))
                    if len(fields) != 3:
                        raise ValueError(f"expected 3 fields, found {len(fields)}")
                    reg, date, status = (part.strip() for part in fields)
                    if not reg or not date or status not in {"P", "A"}:
                        raise ValueError("register/date required and status must be P or A")
                    counts[reg][status] += 1
                except (ValueError, csv.Error) as error:
                    errors.append((path.name, line_no, str(error), raw.rstrip()))
    with open(attendance_out, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Register", "Present", "Absent", "Percentage"])
        for reg, item in sorted(counts.items()):
            total = item["P"] + item["A"]
            pct = item["P"] / total * 100 if total else 0
            writer.writerow([reg, item["P"], item["A"], f"{pct:.2f}"])
    with open(below_out, "w", encoding="utf-8") as file:
        for reg, item in sorted(counts.items()):
            total = item["P"] + item["A"]
            pct = item["P"] / total * 100 if total else 0
            if total and pct < 75:
                file.write(f"{reg},{pct:.2f}%\\n")
    with open(errors_out, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["File", "Line", "Reason", "Original"])
        writer.writerows(errors)
    return counts, errors

def main():
    folder = Path(__file__).with_name("daily_files")
    folder.mkdir(exist_ok=True)
    (folder / "day01.csv").write_text(
        "192311001,2026-10-01,P\\n192311002,2026-10-01,A\\nbroken,line\\n", encoding="utf-8")
    (folder / "day02.csv").write_text(
        "192311001,2026-10-02,A\\n192311002,2026-10-02,P\\n", encoding="utf-8")
    counts, errors = process_month(folder, Path(__file__).with_name("monthly.csv"),
        Path(__file__).with_name("below_75.txt"), Path(__file__).with_name("damaged.csv"))
    print("TASK 2 - ATTENDANCE")
    print("Counts:", dict(counts))
    print("Damaged rows:", errors)
    print("Reports created: monthly.csv, below_75.txt, damaged.csv")

if __name__ == "__main__":
    main()
