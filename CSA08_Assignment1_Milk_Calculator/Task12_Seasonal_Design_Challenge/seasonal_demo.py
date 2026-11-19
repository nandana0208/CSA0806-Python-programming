from decimal import Decimal
from seasonal import seasonal_rate, farmer_ten_day_payment

if __name__ == "__main__":
    print("March standard season rate (4.25, 8.65):",
          seasonal_rate(Decimal("4.25"), Decimal("8.65"), 3))
    print("May seasonal rate (4.25, 8.65):",
          seasonal_rate(Decimal("4.25"), Decimal("8.65"), 5))
    normal = [{"litres": Decimal("100"), "fat": Decimal("4.25"), "snf": Decimal("8.65")}]
    high_volume = [{"litres": Decimal("501"), "fat": Decimal("4.25"), "snf": Decimal("8.65")}]
    print("May 100 L:", farmer_ten_day_payment(normal, 5))
    print("May 501 L incl bonus:", farmer_ten_day_payment(high_volume, 5))
