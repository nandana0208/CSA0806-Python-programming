import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
"""

def load_clean(text):
    """Returns (station, date, pm25) tuples for valid, non-negative readings only."""
    rows = []
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        raw = row["pm25"].strip()
        if raw == "" or raw.upper() == "NA":
            continue
        value = float(raw)
        if value < 0:
            continue
        rows.append((row["station"], row["date"], value))
    return rows

def min_max(values):
    if not values:
        return []
    low, high = min(values), max(values)
    if high == low:
        return [0.0 for _ in values]
    return [round((value - low) / (high - low), 3) for value in values]

clean = load_clean(RAW)
print(clean)
print(min_max([pm for _, _, pm in clean]))
