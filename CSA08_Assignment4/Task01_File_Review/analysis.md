# Task 1 — Diagnosis and design defence

Deficiencies: (1) hard-coded path fails on another PC; (2) no `with` means
exceptions can leave a file open; (3) `read()` loads the whole file into memory;
(4) bare `except: pass` hides both data and programming errors; (5) `int()` rejects
paise such as 1250.50; (6) repeated string `+` repeatedly creates strings;
(7) blank final lines need handling; (8) rejected records are not audited;
(9) missing field validation can cause `IndexError`; (10) encoding is unspecified.

The repair takes a filename parameter, uses UTF-8 and `with`, reads one line at
a time, validates exactly three fields, uses `Decimal` for money and records
the line number, original content and reason for every rejected record.

**Defence (under 100 words):** The repaired version processes one record at a
time, so it does not hold all 50,000 lines in memory. `with` closes the file
reliably. Specific exceptions reject malformed records without hiding unrelated
programming errors. Rejected rows include their line number, original text and
reason, providing an audit trail. `Decimal` handles paise more appropriately
than integer conversion or binary floating-point.

**Alternative:** `read()`/`readlines()` and iteration both take O(n) time.
Reading all content uses O(file size) memory; line iteration uses about
O(one line) working memory, excluding retained report/error results.
