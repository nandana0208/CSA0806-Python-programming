# Task 1 – Understand the Problem and Identify the Data

## Inputs and outputs
Each collection entry stores farmer ID (text identifier), litres (Decimal quantity), fat percentage (Decimal), SNF percentage (Decimal), and shift (Morning/Evening text). A farmer may have multiple entries over ten days and across shifts. For each entry the program computes fat steps, SNF steps, rate per litre and amount payable. The ten-day output is the sum of the rounded entry amounts, plus any applicable bonus in the revised design.

## Constants
The original rate card is BASE_RATE = Rs 30.00, FAT_BASE = 3.5%, SNF_BASE = 8.5%, FAT_STEP_VALUE = Rs 0.40 per 0.1% fat step, and SNF_STEP_VALUE = Rs 0.30 per 0.1% SNF step. The fat acceptance range 2.0%–7.0% is also fixed by the brief. Constants avoid partial rate revisions and make rules visible in one place.

## Types and correctness rules
Farmer ID and shift are strings; litres and percentages are Decimal values because they may contain fractional digits; step counts are integers; money is Decimal quantised to 0.01 rupees. Litres must be positive, fat must be between 2.0 and 7.0 inclusive, and shift must be Morning or Evening. The brief gives no SNF bounds, so the implementation marks 6.0%–10.0% as a replaceable assumption. Numeric fields must be finite and parseable. Duplicate records should be checked using farmer, date/period, shift and collection sequence if the system later supplies those identifiers.

## Assumptions
A 0.1 percentage-point difference is one step. The nearest whole step is used, with decimal ROUND_HALF_UP to avoid binary floating point. Each entry amount is rounded to the nearest paisa before the ten-day total is added. The original brief does not state the SNF validation range or a date schema; both must be confirmed with the co-operative before production deployment.

## Alternative design and complexity
Separate variables such as litres1/fat1/snf1 through litres300/fat300/snf300 make loops, validation and expansion difficult. A list of records (dictionary or dataclass per entry) allows one loop over n entries: O(n) processing and O(n) storage if all entries are retained. Separate named variables also occupy O(n) space but require manually written code proportional to n and do not scale cleanly when n grows to 6,000 or 150,000.
