# Task A1 – Design the Data Acquisition

## A1.1 Inspect the source
A station sends a CSV file with one observation per row. Expected fields are `station`, `date`, `hour`, `pm25`, `pm10`, `no2`, and `temperature`; a temperature-unit field identifies Celsius or Fahrenheit.

Expected data-quality problems include:
- Missing values represented by an empty cell or `NA`, e.g. PM2.5 = `NA`.
- Negative sensor readings, e.g. PM10 = `-12`.
- Implausibly large readings caused by sensor faults, e.g. PM2.5 = `9999`.
- Duplicate observations, e.g. the same station/date/hour repeated.
- Mixed temperature units, e.g. one station sends `86 F` while others send Celsius.
- Inconsistent station labels, e.g. `Adyar`, `ADYAR`, and ` adyar `.
- Invalid dates/hours or non-numeric text in numeric columns.

## A1.2 Design the storage
Use two relational tables:
- `stations(station_id INTEGER PRIMARY KEY, station_name TEXT UNIQUE NOT NULL, temperature_unit TEXT NOT NULL)`.
- `readings(reading_id INTEGER PRIMARY KEY, station_id INTEGER NOT NULL, reading_date TEXT NOT NULL, hour INTEGER NOT NULL, pm25 REAL, pm10 REAL, no2 REAL, temperature_c REAL, UNIQUE(station_id, reading_date, hour), FOREIGN KEY(station_id) REFERENCES stations(station_id))`.

CSV station names map to `stations.station_name`; each reading maps to one `readings` row. Date is stored as ISO `YYYY-MM-DD`, hour as an integer 0–23, and temperature is converted to Celsius before storage. The unique constraint prevents duplicate hourly observations.

## A1.3 CSV or SQL?
1. Average PM2.5 for Adyar in October: CSV requires reading/filtering rows; SQL uses `WHERE station_name=? AND reading_date BETWEEN...` and `AVG(pm25)`.
2. Worst hour by mean PM2.5: CSV requires grouping rows in Python; SQL uses `GROUP BY hour ORDER BY AVG(pm25) DESC`.
3. Compare station averages: CSV requires building a dictionary of totals/counts; SQL uses `GROUP BY station_name`.

For n readings, each CSV/DataFrame question generally scans O(n) rows. An indexed SQL lookup is approximately O(log n) to locate matching rows plus the cost of aggregating those rows. CSV keeps the source on disk but repeated DataFrame loading consumes memory proportional to the loaded data; SQLite stores indexed data on disk and can reuse indexes across questions.
