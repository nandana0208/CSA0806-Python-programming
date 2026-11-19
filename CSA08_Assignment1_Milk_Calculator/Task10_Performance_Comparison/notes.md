# Task 10 – Compare Expectations with Execution

`benchmark.py` measures float, Decimal and integer-paise totals at 300, 6,000 and 150,000 payments with `time.perf_counter()`. Exact output timings depend on the computer and Python build; run the script locally and paste those measured values into the report rather than treating a sample timing as universal.

Float and Decimal may differ by a few ulps after repeated additions. Decimal strings and integer paise are exact for values that are whole paise. The implementation rounds each payment to 0.01 before summing, matching the stated bank-paisa requirement. Rounding only the final sum can differ if unrounded sub-paisa amounts are permitted, so the co-operative must define whether the bank rounds per transaction or per settlement. For a rate-per-litre already rounded to paisa and litres with fractional precision, an individual amount can still contain sub-paise and should be rounded according to the payment policy.

All methods are O(n) time and O(1) accumulator space, excluding the input list. A dictionary cache for k distinct fat/SNF pairs uses O(k) extra space and gives average O(1) lookup per entry after initial rate computation; it helps only if many entries repeat the same pair. Benchmark before adopting it.
