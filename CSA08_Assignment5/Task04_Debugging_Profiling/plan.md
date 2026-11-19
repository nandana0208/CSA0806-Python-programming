# Task A4 – Plan Debugging and Profiling

## A4.1 Debugging plan
- Temporary `print` statements show raw rows, parsed values and rejected records during initial development.
- `assert` statements check invariants such as hours in 0–23, non-negative pollutant readings and unique station/date/hour keys.
- The `logging` module records INFO summaries and WARNING messages for rejected rows; DEBUG details can be enabled only when needed.
- `pdb` or an IDE debugger can pause at parsing/conversion lines, inspect local variables and step through problematic records.

For a finished program, remove temporary prints or gate them behind a debug flag. Logging levels can be changed to WARNING/ERROR without changing program logic.

## A4.2 Profiling plan
Use `time.perf_counter()` around the end-to-end pipeline to measure elapsed wall-clock time. Use `timeit` to repeat a small operation (such as normalisation) and compare implementations. Use `cProfile` to identify functions consuming the most cumulative time. Measurements should be repeated on larger datasets and interpreted with dataset size and machine conditions recorded.

Thousands of print calls can slow execution and clutter output due to console I/O. Logging has configurable levels and can be directed to a file or disabled by raising the threshold. A debugger is interactive and should be used only during diagnosis.
