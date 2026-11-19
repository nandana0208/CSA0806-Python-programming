# Task 4 – Correct Expressions

The conceptual expressions are `fat_steps = round((fat - 3.5) / 0.1)`, `snf_steps = round((snf - 8.5) / 0.1)`, `rate = 30.00 + fat_steps*0.40 + snf_steps*0.30`, and `amount = round(litres*rate, 2)`. The implementation uses Decimal and explicit ROUND_HALF_UP instead of Python's banker's `round()` to make the tie policy explicit.

Unexpected examples:
1. `(4.2 - 3.5) / 0.1` can produce `7.000000000000001` because the decimal operands are binary floats.
2. `0.1 + 0.2 == 0.3` is False because of binary representation.
3. `-7 // 2` is -4 while `int(-7 / 2)` is -3: floor and truncation differ for negatives.
4. `round(2.5)` is 2 in Python because ties go to even; a financial policy may instead require half-up.

`int()` truncates toward zero; `math.floor()` rounds down; `round()` rounds to a chosen number of decimal places and uses ties-to-even by default. For fat 4.2, ideal steps are +7: int on the computed float may produce 7, floor gives 7, round gives 7. For fat 3.1, ideal steps are -4: int(-3.999999...) may produce -3, floor may produce -4, and round may produce -4. Decimal avoids this representation ambiguity. All three operations are O(1) time and O(1) extra space.
