from decimal import Decimal, InvalidOperation

def read_decimal(text, field_name):
    """Parse a decimal string and give a useful error for invalid input."""
    try:
        value = Decimal(text.strip())
    except (InvalidOperation, AttributeError):
        raise ValueError(f"{field_name} must be a number, for example 8.5")
    if not value.is_finite():
        raise ValueError(f"{field_name} must be finite")
    return value

if __name__ == "__main__":
    for sample in ["8.5", " 8.5 ", "8,5", "eight"]:
        try:
            print(repr(sample), "->", read_decimal(sample, "SNF"))
        except ValueError as error:
            print(repr(sample), "-> ERROR:", error)
    amount = Decimal("283.90")
    print(f"Payment: Rs {amount:8.2f}")
