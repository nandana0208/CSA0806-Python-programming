from decimal import Decimal

payments = ["33.40"] * 1000 + ["0.10"] * 3

def total_float(items):
    total = 0.0
    for amount in items:
        total += float(amount)
    return total

def total_decimal(items):
    """Add amount strings exactly using Decimal constructed from strings."""
    total = Decimal("0.00")
    for amount in items:
        total += Decimal(amount)
    return total

if __name__ == "__main__":
    print("float  :", total_float(payments))
    print("Decimal:", total_decimal(payments))
    print(0.1 + 0.2 == 0.3,
          Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
    bad = sum((Decimal(float(x)) for x in ["0.1", "0.2", "0.3"]), Decimal(0))
    print("Decimal(float(...)):", bad)
