"""Central location for the original rate card and validation limits."""
from decimal import Decimal

BASE_RATE = Decimal("30.00")
FAT_BASE_PERCENT = Decimal("3.5")
SNF_BASE_PERCENT = Decimal("8.5")
FAT_STEP_RUPEES = Decimal("0.40")
SNF_STEP_RUPEES = Decimal("0.30")
PERCENT_STEP = Decimal("0.1")
MIN_FAT_PERCENT = Decimal("2.0")
MAX_FAT_PERCENT = Decimal("7.0")
