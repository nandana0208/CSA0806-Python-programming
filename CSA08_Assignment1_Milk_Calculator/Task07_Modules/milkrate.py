"""Rate card module for the Ksheera village milk co-operative."""
from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")

def rate_per_litre(fat, snf):
    """Return the price per litre rounded to two decimal places."""
    fat_steps = ((fat - STANDARD_FAT) / Decimal("0.1")).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP)
    snf_steps = ((snf - STANDARD_SNF) / Decimal("0.1")).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP)
    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
    return rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def payout(litres, fat, snf):
    """Return the farmer payment rounded to the nearest paisa."""
    return (litres * rate_per_litre(fat, snf)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    for litres, fat, snf in [
        (Decimal("10"), Decimal("3.5"), Decimal("8.5")),
        (Decimal("8.5"), Decimal("4.2"), Decimal("8.7")),
        (Decimal("12"), Decimal("3.1"), Decimal("8.3")),
    ]:
        rate = rate_per_litre(fat, snf)
        print(f"{litres:5} L  fat {fat}  snf {snf}  rate {rate:6.2f}  pay {payout(litres, fat, snf):8.2f}")
