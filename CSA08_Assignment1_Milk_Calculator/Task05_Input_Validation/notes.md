# Task 5 – Read Input and Convert Types

`input()` always returns text. Convert identifiers only when numeric semantics are required; keep farmer IDs as strings so leading zeroes are preserved. Parse fractional measurements and money as Decimal. `float("8,5")` raises ValueError because Python expects a dot decimal separator; `float("eight")` also raises ValueError; surrounding whitespace in `" 8.5 "` is accepted by numeric conversion.

Checking with string methods alone is incomplete because signs, decimal points and exponent notation need careful parsing. A `try: Decimal(text) except InvalidOperation` approach is concise, accepts surrounding whitespace and gives one consistent error path. Both approaches take O(1) time per fixed-length entry; exception-based parsing is generally clearer and more robust for user input. Use f-string formatting such as `{amount:8.2f}` for aligned output.
