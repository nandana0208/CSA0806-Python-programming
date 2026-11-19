from decimal import Decimal
from time import perf_counter
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.milkrate import money

def float_sum(items):
    total = 0.0
    for x in items:
        total += float(x)
    return total

def decimal_sum(items):
    total = Decimal("0.00")
    for x in items:
        total += Decimal(x)
    return total

def paise_sum(items):
    return sum(int(Decimal(x) * 100) for x in items)

if __name__ == "__main__":
    print("n       float seconds    Decimal seconds    paise seconds    float-Decimal")
    for n in (300, 6000, 150000):
        values = ["33.40"] * n
        t = perf_counter(); f = float_sum(values); tf = perf_counter() - t
        t = perf_counter(); d = decimal_sum(values); td = perf_counter() - t
        t = perf_counter(); p = paise_sum(values); tp = perf_counter() - t
        print(f"{n:<7} {tf:<15.6f} {td:<18.6f} {tp:<15.6f} {f - float(d):.8f}")
        assert Decimal(p) / 100 == d
    print("Object sizes (bytes):", "float", sys.getsizeof(33.4),
          "Decimal", sys.getsizeof(Decimal("33.40")), "int", sys.getsizeof(3340))
