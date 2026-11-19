"""Season-aware calculator for the revised Day-4 requirement."""
from decimal import Decimal, ROUND_HALF_UP
from datetime import date

CENT = Decimal("0.01")
STEP = Decimal("0.1")
STANDARD_FAT = Decimal("3.5")
STANDARD_SNF = Decimal("8.5")
SNF_STEP_VALUE = Decimal("0.30")

def selected_rate_card(month):
    """Select the seasonal card; April–June changes base and fat-step value."""
    if month in (4, 5, 6):
        return {"base": Decimal("32.00"), "fat_step": Decimal("0.45"),
                "snf_step": SNF_STEP_VALUE}
    return {"base": Decimal("30.00"), "fat_step": Decimal("0.40"),
            "snf_step": SNF_STEP_VALUE}

def step_count(reading, standard):
    """Round a two-decimal analyser reading to nearest 0.1-percent step."""
    return ((reading - standard) / STEP).quantize(
        Decimal("1"), rounding=ROUND_HALF_UP)

def seasonal_rate(fat, snf, month):
    """Calculate rate using the rate card effective for the given month."""
    card = selected_rate_card(month)
    rate = (card["base"] +
            step_count(fat, STANDARD_FAT) * card["fat_step"] +
            step_count(snf, STANDARD_SNF) * card["snf_step"])
    return rate.quantize(CENT, rounding=ROUND_HALF_UP)

def farmer_ten_day_payment(entries, month):
    """Return total payment with Rs 0.50/L bonus if total exceeds 500 L."""
    total_litres = sum((e["litres"] for e in entries), Decimal("0"))
    milk_amount = sum((
        (e["litres"] * seasonal_rate(e["fat"], e["snf"], month)).quantize(
            CENT, rounding=ROUND_HALF_UP) for e in entries
    ), Decimal("0.00"))
    bonus = (total_litres * Decimal("0.50")).quantize(
        CENT, rounding=ROUND_HALF_UP) if total_litres > Decimal("500") else Decimal("0.00")
    return (milk_amount + bonus).quantize(CENT, rounding=ROUND_HALF_UP), bonus
