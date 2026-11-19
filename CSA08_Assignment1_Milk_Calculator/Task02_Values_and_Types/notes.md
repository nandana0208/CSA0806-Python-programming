# Task 2 – Values and Types

Interpreter evidence (representative CPython session):
```pycon
>>> type(10)
<class 'int'>
>>> type(10.0)
<class 'float'>
>>> type("10")
<class 'str'>
>>> type(True)
<class 'bool'>
>>> type([10, 8.5])
<class 'list'>
>>> 7 / 2
3.5
>>> 7 // 2
3
>>> 7 % 2
1
>>> -7 // 2
-4
>>> 0.1 + 0.2 == 0.3
False
```
`/` performs true division, `//` floors the quotient, `%` returns the remainder, and floor division rounds toward negative infinity (so -7 // 2 is -4). Float values use finite binary representations, so 0.1 and 0.2 cannot be represented exactly and their sum is not exactly the same stored value as 0.3.

Money should not be accumulated as float. `round()` can format a float but cannot restore information already lost during arithmetic. Integer paise are exact when every amount is expressed in whole paise. `Decimal` constructed from strings is also exact for decimal currency and supports explicit rounding rules. The completed TODO is in `interpreter_and_decimal.py`; compare `Decimal(amount)` with `Decimal(float(amount))`, which imports the float's binary approximation and therefore exposes extra digits.
