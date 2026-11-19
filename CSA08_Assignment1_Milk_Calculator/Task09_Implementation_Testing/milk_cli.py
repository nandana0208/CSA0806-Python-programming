from calculator import make_entry, format_payment
from common.milkrate import ten_day_total

def main():
    """Read collection records interactively and print the ten-day total."""
    entries = []
    print("Ksheera Milk Co-operative – collection entry")
    while True:
        farmer = input("Farmer ID (blank to finish): ").strip()
        if not farmer:
            break
        try:
            litres = input("Litres: ")
            fat = input("Fat %: ")
            snf = input("SNF %: ")
            shift = input("Shift (Morning/Evening): ")
            entry = make_entry(farmer, litres, fat, snf, shift)
            entries.append(entry)
            print(format_payment(entry))
        except Exception as error:
            print("Entry not accepted:", error)
    print("Ten-day total: Rs", ten_day_total(entries))

if __name__ == "__main__":
    main()
