# Task 4 — Forensics

Mode `w` truncates the previous log each day. Missing newline characters join
book titles. If `write()` raises before manual `close()`, the file may remain
open and buffered data may not be flushed. The test runs three days and prints
the faulty and repaired logs.

Repair rules: use `with` for every file; use append mode for a continuing log;
write an explicit newline after each record; save failures in an error log.

Manual `try/finally` can also close files. It does not change O(n) time or
streaming O(1) working space. A `with` block and a correct `finally` both close
the file; without either, repeated failures can leave multiple files open.
