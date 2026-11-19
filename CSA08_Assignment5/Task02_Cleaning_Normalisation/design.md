# Task A2 – Design the Cleaning and Normalisation

## A2.1 Cleaning rules
- Missing blank/`NA` readings: retain as missing during inspection, then omit that measurement from its metric's average rather than inventing a value. For a time series where continuity is essential, forward-fill may be considered but should be flagged.
- Impossible readings: discard negative values and values above configured sensor sanity limits; preserve a rejection count for audit.
- Duplicate rows: keep one observation for each station/date/hour using a unique key.
- Fahrenheit: convert using `(F - 32) * 5 / 9` before analysis.
- Station names: trim whitespace and use title case to make matching consistent.

The sample implementation uses explicit sanity limits (PM2.5 0–1000, PM10 0–2000, NO2 0–2000, temperature -50–60 °C) as demonstration assumptions; real limits should follow the board's sensor specification.

## A2.2 Normalisation
Min-max normalisation: `x_scaled = (x - min(x)) / (max(x) - min(x))`. It maps values to 0–1 and is useful when a bounded scale is required. If all values are equal, return 0 for each value to avoid division by zero.

Z-score standardisation: `z = (x - mean(x)) / population_std(x)`. It centres values at zero with unit standard deviation and is useful when comparing deviations from the mean. If standard deviation is zero, return zero.

## A2.3 Formatting
Dates use ISO `YYYY-MM-DD`; station names use trimmed title case; hours are integers 0–23; pollutant values are numeric floating-point values rounded to a consistent display precision; temperature is always Celsius.

Dropping missing observations avoids fabricated values but may reduce sample size and can bias daily means if missingness is systematic. Dropping and forward-fill are O(n); sorting to calculate a median is O(n log n). Streaming cleaning needs O(1) auxiliary space, while retaining all values for median/analysis requires O(n) space.
