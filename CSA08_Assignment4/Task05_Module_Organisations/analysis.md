# Task 5 — Compare the organisations

| Form | Strength | Limitation |
|---|---|---|
| One script | Simple to start and find code | Crowded as features grow |
| One utility module + main | Reusable helpers | Concerns still grouped together |
| Three modules | Reader/statistics/report are separated | More files to navigate |
| Package | Clear namespace and scalable testing | Slight setup/import structure |

The consecutive-absence feature can live in the same script (one file), helper
module (one or two files), statistics/report modules, or package `stats.py` and
`report.py` (plus main if its calls change). Exact files changed depend on API
design.

`import attendance.stats` accesses the qualified submodule;
`from attendance import stats` imports the submodule name from the package;
`from attendance.stats import percentage` imports the function directly.
Python caches imported modules in `sys.modules`; initial import has a one-time
time/memory cost. Actual attendance calculations retain their algorithmic
complexity. A package makes finding and changing a responsibility easier.
