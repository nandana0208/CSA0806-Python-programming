import csv
import sqlite3
import statistics
import logging
import time
import timeit
import cProfile
import re
from pathlib import Path
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
DATA = BASE / "data" / "air_quality.csv"
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)
DB = OUT / "air_quality.db"
CLEAN_CSV = OUT / "cleaned_air_quality.csv"
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOG = logging.getLogger("air-quality")

LIMITS = {"pm25": (0, 1000), "pm10": (0, 2000), "no2": (0, 2000),
          "temperature_c": (-50, 60)}

def normalise_station(value):
    return value.strip().title()

def to_float(value):
    if value is None or value.strip().upper() in ("", "NA", "N/A", "NULL"):
        return None
    try:
        return float(value)
    except ValueError:
        return None

def min_max(values):
    if not values:
        return []
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.0 for _ in values]
    return [round((v - lo) / (hi - lo), 3) for v in values]

def z_scores(values):
    if not values:
        return []
    mean = statistics.mean(values)
    sd = statistics.pstdev(values)
    if sd == 0:
        return [0.0 for _ in values]
    return [round((v - mean) / sd, 3) for v in values]

def clean_rows(path):
    cleaned, rejected, seen = [], Counter(), set()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            station = normalise_station(row["station"])
            try:
                date = row["date"].strip()
                hour = int(row["hour"])
                # Validate ISO date and hour.
                from datetime import date as date_type
                date_type.fromisoformat(date)
                assert 0 <= hour <= 23
            except (ValueError, AssertionError):
                rejected["invalid_date_or_hour"] += 1
                continue

            unit = row.get("temperature_unit", "C").strip().upper()
            temp = to_float(row.get("temperature"))
            if temp is not None and unit == "F":
                temp = (temp - 32) * 5 / 9
            elif unit not in ("C", "F"):
                rejected["unknown_temperature_unit"] += 1
                temp = None

            values = {}
            for field in ("pm25", "pm10", "no2"):
                value = to_float(row.get(field))
                lo, hi = LIMITS[field]
                if value is not None and not lo <= value <= hi:
                    rejected[field + "_out_of_range"] += 1
                    value = None
                values[field] = value
            lo, hi = LIMITS["temperature_c"]
            if temp is not None and not lo <= temp <= hi:
                rejected["temperature_out_of_range"] += 1
                temp = None

            key = (station, date, hour)
            if key in seen:
                rejected["duplicate"] += 1
                continue
            seen.add(key)
            cleaned.append({"station": station, "date": date, "hour": hour,
                            **values, "temperature_c": round(temp, 2) if temp is not None else None})
    LOG.info("Rows accepted: %d | rejected/flagged: %s", len(cleaned), dict(rejected))
    return cleaned, rejected

def store_and_query(rows):
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript("""
        CREATE TABLE stations(
            station_id INTEGER PRIMARY KEY,
            station_name TEXT UNIQUE NOT NULL
        );
        CREATE TABLE readings(
            reading_id INTEGER PRIMARY KEY,
            station_id INTEGER NOT NULL,
            reading_date TEXT NOT NULL,
            hour INTEGER NOT NULL CHECK(hour BETWEEN 0 AND 23),
            pm25 REAL, pm10 REAL, no2 REAL, temperature_c REAL,
            UNIQUE(station_id, reading_date, hour),
            FOREIGN KEY(station_id) REFERENCES stations(station_id)
        );
    """)
    stations = sorted({r["station"] for r in rows})
    con.executemany("INSERT INTO stations(station_name) VALUES (?)",
                    [(s,) for s in stations])
    station_ids = dict(con.execute("SELECT station_name, station_id FROM stations"))
    payload = [(station_ids[r["station"]], r["date"], r["hour"], r["pm25"],
                r["pm10"], r["no2"], r["temperature_c"]) for r in rows]
    con.executemany("""INSERT INTO readings
        (station_id, reading_date, hour, pm25, pm10, no2, temperature_c)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", payload)
    con.commit()

    q1 = con.execute("""SELECT AVG(r.pm25) FROM readings r
        JOIN stations s USING(station_id)
        WHERE s.station_name=? AND r.reading_date BETWEEN ? AND ?""",
        ("Adyar", "2026-10-01", "2026-10-31")).fetchone()[0]
    q2 = con.execute("""SELECT s.station_name, AVG(r.pm25) AS avg_pm25
        FROM readings r JOIN stations s USING(station_id)
        GROUP BY s.station_name ORDER BY avg_pm25 DESC""").fetchall()
    q3 = con.execute("""SELECT hour, AVG(pm25) AS avg_pm25 FROM readings
        WHERE pm25 IS NOT NULL GROUP BY hour ORDER BY avg_pm25 DESC""").fetchall()
    daily = con.execute("""SELECT s.station_name, r.reading_date,
        MIN(r.pm25), MAX(r.pm25), AVG(r.pm25), COUNT(r.pm25)
        FROM readings r JOIN stations s USING(station_id)
        GROUP BY s.station_name, r.reading_date
        ORDER BY r.reading_date, s.station_name""").fetchall()
    con.close()
    return q1, q2, q3, daily

def save_clean_csv(rows):
    fields = ["station", "date", "hour", "pm25", "pm10", "no2", "temperature_c"]
    with CLEAN_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def make_charts(rows, q2, q3):
    # Monthly/date trend (one point per date, averaged across available stations).
    by_date = {}
    for r in rows:
        if r["pm25"] is not None:
            by_date.setdefault(r["date"], []).append(r["pm25"])
    dates = sorted(by_date)
    means = [statistics.mean(by_date[d]) for d in dates]
    plt.figure()
    plt.plot(dates, means, marker="o")
    plt.title("Daily Mean PM2.5 – October 2026")
    plt.xlabel("Date"); plt.ylabel("PM2.5 (µg/m³)")
    plt.xticks(rotation=30); plt.tight_layout()
    plt.savefig(OUT/"pm25_monthly_trend.png"); plt.close()

    plt.figure()
    plt.bar([x[0] for x in q2], [x[1] for x in q2])
    plt.title("Average PM2.5 by Station")
    plt.xlabel("Station"); plt.ylabel("Mean PM2.5 (µg/m³)")
    plt.tight_layout(); plt.savefig(OUT/"station_comparison.png"); plt.close()

    pairs = [(r["temperature_c"], r["pm25"]) for r in rows
             if r["temperature_c"] is not None and r["pm25"] is not None]
    plt.figure()
    if pairs:
        plt.scatter([x for x, _ in pairs], [y for _, y in pairs])
    plt.title("Temperature vs PM2.5")
    plt.xlabel("Temperature (°C)"); plt.ylabel("PM2.5 (µg/m³)")
    plt.tight_layout(); plt.savefig(OUT/"temperature_vs_pm25.png"); plt.close()

    plt.figure()
    plt.bar([str(x[0]) for x in q3], [x[1] for x in q3])
    plt.title("Average PM2.5 by Hour")
    plt.xlabel("Hour of day"); plt.ylabel("Mean PM2.5 (µg/m³)")
    plt.tight_layout(); plt.savefig(OUT/"worst_hours.png"); plt.close()

def sentiment_score(text):
    positive = {"good": 1, "clean": 1, "improved": 2, "better": 1, "safe": 1}
    negative = {"bad": -1, "smoke": -1, "unsafe": -2, "polluted": -2,
                "dirty": -1, "worse": -1}
    tokens = re.findall(r"[a-z']+", text.lower())
    score, negate = 0, False
    for token in tokens:
        if token in {"not", "never", "no"}:
            negate = True
            continue
        value = positive.get(token, negative.get(token, 0))
        score += -value if negate else value
        negate = False
    return score

def extractive_summary(text, sentence_count=2):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    stop = {"the", "and", "is", "in", "to", "of", "a", "it", "was", "are", "for"}
    words = re.findall(r"[a-z]+", text.lower())
    freq = Counter(w for w in words if w not in stop)
    if not sentences or not freq:
        return ""
    ranked = sorted(enumerate(sentences),
                    key=lambda item: sum(freq[w] for w in re.findall(r"[a-z]+", item[1].lower())),
                    reverse=True)
    chosen = sorted(i for i, _ in ranked[:sentence_count])
    return " ".join(sentences[i] for i in chosen)

def chatbot(question, con):
    q = question.lower()
    station_names = [r[0] for r in con.execute("SELECT station_name FROM stations")]
    station = next((s for s in station_names if s.lower() in q), None)
    pollutant = next((p for p in ("pm25", "pm2.5", "pm10", "no2") if p in q), None)
    if not station or not pollutant:
        return "Please include a known station name and pollutant (PM2.5, PM10 or NO2)."
    column = "pm25" if pollutant == "pm2.5" else pollutant
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", q)
    day = date_match.group(0) if date_match else "2026-10-01"
    value = con.execute(f"""SELECT AVG(r.{column}) FROM readings r
        JOIN stations s USING(station_id)
        WHERE s.station_name=? AND r.reading_date=?""", (station, day)).fetchone()[0]
    if value is None:
        return f"No {pollutant.upper()} reading is available for {station} on {day}."
    return f"Average {pollutant.upper()} for {station} on {day}: {value:.1f}."

def main():
    start = time.perf_counter()
    rows, rejected = clean_rows(DATA)
    assert all(0 <= r["hour"] <= 23 for r in rows)
    assert len({(r["station"], r["date"], r["hour"]) for r in rows}) == len(rows)
    assert all(r["pm25"] is None or r["pm25"] >= 0 for r in rows)
    save_clean_csv(rows)
    q1, q2, q3, daily = store_and_query(rows)
    make_charts(rows, q2, q3)

    complaints = [
        "The air is bad and smoke is everywhere near the road.",
        "The air is not good today, but monitoring has improved.",
        "Our neighbourhood is clean and safe now."
    ]
    sentiment = [(c, sentiment_score(c)) for c in complaints]
    summary = extractive_summary(" ".join(complaints))
    con = sqlite3.connect(DB)
    answer = chatbot("What is the PM2.5 in Adyar today?", con)
    con.close()

    elapsed = time.perf_counter() - start
    norm_time = timeit.timeit(lambda: min_max([12, 25, 40, 52, 80]), number=1000)
    report = OUT/"execution_report.txt"
    with report.open("w", encoding="utf-8") as f:
        f.write("ASSIGNMENT 5 – EXECUTION REPORT\n")
        f.write(f"Accepted observations: {len(rows)}\n")
        f.write(f"Rejected/flagged counts: {dict(rejected)}\n")
        f.write(f"Adyar October average PM2.5: {q1:.2f}\n" if q1 is not None else "Adyar October average PM2.5: unavailable\n")
        f.write(f"Station averages: {q2}\n")
        f.write(f"Worst hours by average PM2.5: {q3}\n")
        f.write(f"Daily summaries: {daily}\n")
        f.write(f"Sentiment scores: {sentiment}\n")
        f.write(f"Extractive summary: {summary}\n")
        f.write(f"Chatbot: {answer}\n")
        f.write(f"Elapsed seconds: {elapsed:.6f}\n")
        f.write(f"1000 min-max runs seconds: {norm_time:.6f}\n")
        f.write("Charts: pm25_monthly_trend.png, station_comparison.png, temperature_vs_pm25.png, worst_hours.png\n")
    profiler = cProfile.Profile()
    profiler.enable()
    for _ in range(100):
        min_max([12, 25, 40, 52, 80])
    profiler.disable()
    profiler.dump_stats(OUT/"profile.stats")
    print(f"Accepted observations: {len(rows)}")
    print(f"Rejected/flagged: {dict(rejected)}")
    print(f"Adyar October average PM2.5: {q1:.2f}")
    print(f"Station averages: {q2}")
    print(f"Chatbot: {answer}")
    print(f"Sentiment scores: {[score for _, score in sentiment]}")
    print(f"Elapsed seconds: {elapsed:.4f}")
    print(f"Outputs saved in: {OUT}")

if __name__ == "__main__":
    main()
