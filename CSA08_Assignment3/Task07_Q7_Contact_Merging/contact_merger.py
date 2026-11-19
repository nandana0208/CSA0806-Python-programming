"""Q7 - Merge contacts using normalised phone numbers as dictionary keys."""

import random
import re
import time


CONTACTS = [
    {"name": "Dr. Ravi", "phone": "+91 98400 12345", "email": "ravi@example.com"},
    {"name": "Ravi Kumar", "phone": "9840012345", "email": "rk@example.com"},
    {"name": "Meena", "phone": "+91-90000-11111", "email": "meena@example.com"},
    {"name": "Arun", "phone": "", "email": "arun@example.com"},
    {"name": "Arun", "phone": None, "email": "arun.work@example.com"},
    {"name": "Kavya", "phone": "98888 22222", "email": ""},
]


def normalize_phone(phone):
    """Keep digits and remove India's leading country code for comparison."""
    digits = re.sub(r"\D", "", phone or "")
    if digits.startswith("91") and len(digits) > 10:
        digits = digits[2:]
    return digits


def normalize_name(name):
    """Use a simple lowercase alphabetic form for display matching support."""
    return " ".join(re.findall(r"[a-z]+", (name or "").lower()))


def merge_contacts(contacts):
    merged = {}
    no_phone = []

    for contact in contacts:
        phone = normalize_phone(contact.get("phone"))
        email = (contact.get("email") or "").strip().lower()
        name = (contact.get("name") or "Unknown").strip()

        if not phone:
            # Without a phone number we cannot safely use it as the identity key.
            no_phone.append({
                "name": name,
                "numbers": set(),
                "emails": {email} if email else set(),
            })
            continue

        if phone not in merged:
            merged[phone] = {
                "name": name,
                "normalised_name": normalize_name(name),
                "numbers": set(),
                "emails": set(),
            }

        merged[phone]["numbers"].add(phone)
        if email:
            merged[phone]["emails"].add(email)

        # Prefer the more descriptive name when two records share a number.
        if len(name) > len(merged[phone]["name"]):
            merged[phone]["name"] = name

    return list(merged.values()) + no_phone


def benchmark(size):
    sample = []
    for index in range(size):
        number = f"90000{index % max(1, size // 2):05d}"
        sample.append({
            "name": f"Contact {index}",
            "phone": number,
            "email": f"user{index}@example.com",
        })
    start = time.perf_counter()
    result = merge_contacts(sample)
    elapsed = time.perf_counter() - start
    return elapsed, len(result)


def main():
    merged = merge_contacts(CONTACTS)
    print("Q7 - CONTACT MERGING")
    for contact in merged:
        print(f"{contact['name']}:")
        print("  numbers:", sorted(contact["numbers"]))
        print("  emails :", sorted(contact["emails"]))

    print("\nSame phone, different spelling merged:",
          len(merged[0]["emails"]) == 2)
    print("Missing phone records are kept separately:", sum(
        not item["numbers"] for item in merged
    ))

    print("\nPerformance test (generated contacts):")
    for size in (1_000, 100_000):
        elapsed, unique_contacts = benchmark(size)
        print(f"{size:>6} input contacts -> {unique_contacts:>6} merged groups "
              f"in {elapsed:.5f}s")

    print("\nDesign note:")
    print("- Dictionary grouping is O(n) average, rather than comparing every pair O(n^2).")
    print("- Two people with the same name stay separate when their phone numbers differ.")
    print("- Limitation: shared or recycled phone numbers can incorrectly merge people.")
    print("- Records without a phone are retained separately to avoid unsafe name-only merging.")


if __name__ == "__main__":
    main()
