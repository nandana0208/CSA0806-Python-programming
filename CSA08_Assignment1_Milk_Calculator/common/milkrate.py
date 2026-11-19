"""Reusable, exact-rupee milk payment calculations."""
from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
FAT_BASE = Decimal("3.5")
SNF_BASE = Decimal("8.5")
FAT_STEP = Decimal("0.1")
SNF_STEP = Decimal("0.1")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
MIN_FAT = Decimal("2.0")
MAX_FAT = Decimal("7.0")
# Assumption only: replace with the co-operative's official SNF limits.
MIN_SNF = Decimal("6.0")
MAX_SNF = Decimal("10.0")
CENT = Decimal("0.01")
ONE = Decimal("1")

def money(value):
    """Round a rupee amount to the nearest paisa using half-up rounding."""
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)

def whole_steps(reading, standard, step):
    """Return nearest whole 0.1-percent steps, with decimal-safe arithmetic."""
    return ((reading - standard) / step).quantize(ONE, rounding=ROUND_HALF_UP)

def validate_entry(farmer_id, litres, fat, snf, shift):
    """Raise ValueError when an entry violates the stated input rules."""
    if not farmer_id.strip():
        raise ValueError("Farmer ID cannot be empty.")
    if litres <= 0:
        raise ValueError("Litres must be greater than zero.")
    if not MIN_FAT <= fat <= MAX_FAT:
        raise ValueError(f"Fat must be between {MIN_FAT} and {MAX_FAT}%.")
    if not MIN_SNF <= snf <= MAX_SNF:
        raise ValueError(f"SNF must be between {MIN_SNF} and {MAX_SNF}% (sample assumption).")
    if shift.strip().lower() not in {"morning", "evening"}:
        raise ValueError("Shift must be Morning or Evening.")

def rate_per_litre(fat, snf, rate_card=None):
    """Calculate a paisa-rounded litre rate using the selected rate card."""
    card = rate_card or {
        "base": BASE_RATE, "fat_step": FAT_STEP_VALUE,
        "snf_step": SNF_STEP_VALUE, "fat_base": FAT_BASE,
        "snf_base": SNF_BASE, "step": FAT_STEP
    }
    fat_steps = whole_steps(fat, card["fat_base"], card["step"])
    snf_steps = whole_steps(snf, card["snf_base"], card["step"])
    return money(card["base"] + fat_steps * card["fat_step"] +
                 snf_steps * card["snf_step"])

def payout(litres, fat, snf, rate_card=None):
    """Return the payment for one entry, rounded to two decimal places."""
    return money(litres * rate_per_litre(fat, snf, rate_card))

def ten_day_total(entries):
    """Return the sum of already rounded entry payments."""
    return money(sum((payout(e["litres"], e["fat"], e["snf"])
                      for e in entries), Decimal("0.00")))

def paise_total(amounts):
    """Sum money by converting each exact decimal rupee amount to integer paise."""
    return sum(int((money(a) * 100).to_integral_exact()) for a in amounts)
