# Task 12 – Re-evaluate and Adapt the Design

## A. Impact analysis
The analyser now provides two decimal places, seasonal rates apply April–June, and a farmer supplying more than 500 L in ten days receives Rs 0.50 per litre. The constants for seasonal base and fat step change; the rate-selection function and ten-day settlement function are affected. Decimal step arithmetic remains suitable: `(4.25 - 3.5) / 0.1 = 7.5`, and the implementation explicitly rounds half-up to 8 steps. This tie rule must be approved by the co-operative because the brief says nearest whole step but does not define ties.

## B. Evaluate the original design
The original Decimal approach, named constants and module remain appropriate, but a single fixed rate card is no longer sufficient. A rate-card selector and bonus function are added. For 4.25% fat and 8.65% SNF, March uses 8 fat steps and 2 SNF steps: Rs 30 + 8×0.40 + 2×0.30 = Rs 33.80/L. May uses Rs 32 + 8×0.45 + 2×0.30 = Rs 36.20/L.

## C. Adaptation
`seasonal.py` selects a rate card by month, calculates decimal-safe steps, rounds each entry amount to paisa and applies Rs 0.50/L to all ten-day litres only when total litres are strictly greater than 500. The original SNF adjustment remains Rs 0.30 because no seasonal SNF revision is specified.

## D. Evidence-based defence
Run `python seasonal_demo.py`. It checks a standard-season rate, seasonal rate, a farmer below the bonus threshold and a farmer above it. The modular design retains the original calculation structure and isolates seasonal policy. For production, select season by the collection date rather than a manually supplied month, define how a ten-day period crossing a season boundary is treated, and version the rate card. The threshold test is strictly `> 500`, not `>= 500`.
