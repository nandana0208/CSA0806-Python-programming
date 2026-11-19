# Task 6 – Organise the Logic into Functions

`rate_per_litre(fat, snf)` returns a Decimal rupees-per-litre value. `payout(litres, fat, snf)` returns one rounded payment. `ten_day_total(entries)` returns the sum of rounded entry payments. `validate_entry(...)` checks the business rules. Every function has a docstring in `common/milkrate.py`.

Returning a value lets the caller test, combine, store or print it. Printing inside a calculation function couples business logic to the screen and makes reuse harder. Rate constants are module globals that functions may read; they should not be reassigned inside functions. Local names exist only during a call, while global names are defined at module scope.

One long script repeats logic and is harder to test. Lambda expressions are best for short one-expression functions and are not a replacement for named multi-step business rules. Function calls add a small constant overhead, so processing n entries remains O(n); the overhead is negligible compared with validation, I/O and database work.
