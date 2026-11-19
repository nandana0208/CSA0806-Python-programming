"""Q4 - Find elective registration clashes with set operations."""

import random
import time


def main():
    ai_elective = {"192311001", "192311004", "192311007", "192311009"}
    iot_elective = {"192311002", "192311004", "192311009", "192311010"}
    all_students = {f"1923110{i:02d}" for i in range(1, 11)}

    both = ai_elective & iot_elective
    exactly_one = ai_elective ^ iot_elective
    neither = all_students - (ai_elective | iot_elective)

    print("Q4 - ELECTIVE REGISTRATION")
    print("clash      :", sorted(both))
    print("exactly one:", sorted(exactly_one))
    print("neither    :", sorted(neither))

    # The method-based version gives the same three answers.
    both_method = ai_elective.intersection(iot_elective)
    one_method = ai_elective.symmetric_difference(iot_elective)
    neither_method = all_students.difference(ai_elective.union(iot_elective))
    print("\nSet-method results match:", (both, exactly_one, neither) ==
          (both_method, one_method, neither_method))

    print("\nDuplicate removal:", len(["A", "A", "B"]), "list items ->",
          len(set(["A", "A", "B"])), "unique set items")
    print("Empty intersection:", set() & ai_elective)
    print("Identical elective symmetric difference:", ai_elective ^ ai_elective)

    print("\nMembership timing (seconds; one lookup):")
    for size in (10_000, 100_000, 1_000_000):
        values = list(range(size))
        value_set = set(values)
        target = size - 1
        start = time.perf_counter()
        target in values
        list_time = time.perf_counter() - start
        start = time.perf_counter()
        target in value_set
        set_time = time.perf_counter() - start
        print(f"{size:>9}: list {list_time:.8f} | set {set_time:.8f}")

    print("\nComplexity: set membership/intersection is O(1) average per lookup / O(n) operation.")
    print("Converting a list to a set removes duplicates and does not preserve positional order.")


if __name__ == "__main__":
    main()
