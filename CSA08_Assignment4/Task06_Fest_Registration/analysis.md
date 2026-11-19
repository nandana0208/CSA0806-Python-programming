# Task 6 — Design challenge

Inputs are five department text files; each valid row contains register number,
name, department, email and semicolon-separated events. Outputs are a deduplicated
master CSV, one participant CSV per event, summary and error log.

Testable requirements: valid register numbers appear once; duplicate rows merge
events and email addresses; invalid emails/damaged rows are logged with file and
line; missing/unreadable files are logged and do not stop other files.

Flow: list files -> read lines -> validate fields/email -> check seen-register
set -> merge duplicate or add to master dictionary -> group by event -> write
master/event/summary/error reports.

Package structure: `reader.py` reads lines; `validator.py` checks data and raises
`InvalidRegistration`; `processor.py` coordinates deduplication and outputs;
`run_fest.py` is the entry point. Email validation uses `strip`, `count`,
`split`, `startswith` and `endswith`. Per-line custom errors are caught around
each record; file errors are caught around each file.

Pseudocode: initialise master, seen set and error list; for every department
file, read each line; validate; if register is in seen, merge event/email sets;
otherwise add to seen and master; catch invalid row and log it; catch file-level
errors and continue; write master, event files, summary and error log.

Duplicate lookup using a set is O(1) average, giving O(n) average processing
for n registrations (plus output work). Searching a list of previous records
for each new record is O(n²). Both approaches use O(n) storage.
