# Task 3 – Variables and Constants

Python identifiers may contain letters, digits and underscores but cannot start with a digit or be a keyword. Use descriptive `snake_case` names for variables and `UPPER_CASE` for module-level constants. Python does not enforce immutable constants; the uppercase convention communicates that a value should not be reassigned.

Dynamic typing means `value = 10` binds an integer and `value = "ten"` later binds a string. The name is rebound; Python does not permanently declare its type. Multiple assignment can unpack values and swap them without a temporary variable: `a, b = b, a`.

The rate card is centralised in `constants.py` and in `common/milkrate.py`. Hard-coded magic numbers require k separate edits for k occurrences and risk inconsistent revisions. A dictionary rate card is also valid and makes seasonal selection convenient. Both approaches have O(1) lookup/calculation for a fixed number of fields; the runtime difference is negligible, while centralised configuration greatly reduces maintenance risk.
