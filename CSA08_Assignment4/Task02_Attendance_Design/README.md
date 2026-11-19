# Task 2 — Data and file-operation design

Input format: `register_number,date,P-or-A`. A dictionary maps register numbers
to present/absent counters. A list stores damaged rows with file, line number,
reason and original text.

Outputs: `monthly.csv` (counts and percentage), `below_75.txt` (students below
75%) and `damaged.csv` (audit trail). Use `pathlib.Path.glob` to list daily
files, UTF-8, `r` for input and `w` for generated reports. Iterate line-by-line;
`csv.reader` parses records and `csv.writer` writes report rows. Append mode `a`
is useful for persistent logs across multiple runs.

Pseudocode: initialise counts and errors; for each daily file, open and iterate
with line numbers; validate 3 fields and P/A status; increment dictionary
counter for valid records; catch invalid records and append audit details;
after all files, calculate percentages and write the three reports.

Trace: `192311001,2026-10-01,P` increments P; `192311002,2026-10-01,A`
increments A; `broken,line` has two fields and is recorded as damaged.

Alternative: rereading all f files of l lines for each of s students costs
O(s*f*l); one pass with a dictionary costs O(f*l) average time and O(s)
counter storage plus errors.
