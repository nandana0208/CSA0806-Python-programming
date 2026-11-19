from decimal import Decimal
import milkrate as mr

if __name__ == "__main__":
    print("Imported rate:", mr.rate_per_litre(Decimal("4.2"), Decimal("8.7")))
    print("Imported payout:", mr.payout(Decimal("8.5"), Decimal("4.2"), Decimal("8.7")))
