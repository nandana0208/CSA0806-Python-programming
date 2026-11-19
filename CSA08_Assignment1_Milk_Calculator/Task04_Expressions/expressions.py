from decimal import Decimal, ROUND_HALF_UP

def steps(value, standard):
    """Count nearest 0.1 percentage-point steps without binary float error."""
    return ((value - standard) / Decimal("0.1")).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    fat, snf = Decimal("4.2"), Decimal("8.7")
    fat_steps = steps(fat, Decimal("3.5"))
    snf_steps = steps(snf, Decimal("8.5"))
    rate = Decimal("30.00") + fat_steps * Decimal("0.40") + snf_steps * Decimal("0.30")
    amount = (Decimal("8.5") * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    print("fat steps:", fat_steps, "snf steps:", snf_steps)
    print("rate:", rate, "amount:", amount)
    print("(4.2 - 3.5) / 0.1 =", (4.2 - 3.5) / 0.1)
    print("int(0.7 / 0.1) =", int(0.7 / 0.1))
    print("round(0.7 / 0.1) =", round(0.7 / 0.1))
    print("round(-1.5) =", round(-1.5), "int(-1.5) =", int(-1.5))
    print("-7 // 2 =", -7 // 2, "int(-7 / 2) =", int(-7 / 2))
