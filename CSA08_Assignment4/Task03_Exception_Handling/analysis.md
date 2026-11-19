# Task 3 — Failure and exception analysis

| Failure | Exception / response |
|---|---|
| Missing folder or file | `FileNotFoundError` |
| Permission denied | `PermissionError` |
| Wrong text encoding | `UnicodeDecodeError` |
| Wrong field count/status | Custom `InvalidRecord` |
| Empty file | No exception; zero counts |
| Accessing a missing field | `IndexError`, prevented by field-count check |
| Invalid numeric text | `ValueError` |

`parse_line` raises `InvalidRecord`; `summarise` catches it for each row and
continues. File-level exceptions are handled outside the row loop. `else`
processes only valid records; `finally` is present, while `with` guarantees
closure. `raise ... from ...` preserves the original cause.

Misuse experiment: replacing specific handlers with `except Exception: pass`
can hide a typo such as `presnt += 1` (NameError). The program silently skips
the count and gives misleading results.

Alternative: EAFP attempts parsing and catches invalid data; LBYL checks fields
before using them. Both are O(1) per row and O(n) for n rows. EAFP is concise
when bad rows are rare; LBYL can be clearer when validation is extensive.
