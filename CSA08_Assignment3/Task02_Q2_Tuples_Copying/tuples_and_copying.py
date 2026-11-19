"""Q2 - Tuples, mutability, aliasing and copying."""

import copy
import sys
import time


def main():
    rows, cols = 3, 4

    bad = [[0] * cols] * rows
    bad[0][1] = 7

    # Each iteration creates a fresh row, so rows do not share one list.
    good = [[0 for _ in range(cols)] for _ in range(rows)]
    good[0][1] = 7

    print("Q2 - TUPLES AND COPYING")
    print("bad :", bad)
    print("good:", good)
    print("Row identity (bad, good):", bad[0] is bad[1], good[0] is good[1])

    stops = {
        (13.0827, 80.2707): "Chennai Central",
        (13.0418, 80.2341): "T. Nagar",
    }
    print("Stop lookup:", stops[(13.0418, 80.2341)])

    print("\nAliasing and copying:")
    original = [[1, 2], [3, 4]]
    alias = original
    shallow = copy.copy(original)
    sliced = original[:]
    deep = copy.deepcopy(original)
    original[0][0] = 99
    print("Alias sees change:", alias)
    print("Shallow copy shares inner row:", shallow)
    print("Slice shares inner row:", sliced)
    print("Deep copy stays independent:", deep)
    print("Identity checks:", original is alias, original is shallow,
          original[0] is shallow[0], original[0] is deep[0])

    print("\nTuple unpacking:")
    for (coordinate, place) in stops.items():
        latitude, longitude = coordinate
        print(f"{place}: latitude={latitude}, longitude={longitude}")

    print("\nA list inside a tuple can still change:")
    mixed = ([10, 20], "fixed outer tuple")
    mixed[0].append(30)
    print(mixed)

    print("\nMemory and basic timing (values are machine-dependent):")
    values = list(range(1_000_000))
    tuple_values = tuple(values)
    print("List container bytes:", sys.getsizeof(values))
    print("Tuple container bytes:", sys.getsizeof(tuple_values))

    start = time.perf_counter()
    list_copy = list(range(100_000))
    list_create = time.perf_counter() - start
    start = time.perf_counter()
    tuple_copy = tuple(range(100_000))
    tuple_create = time.perf_counter() - start
    start = time.perf_counter()
    _ = list_copy[50_000]
    list_index = time.perf_counter() - start
    start = time.perf_counter()
    _ = tuple_copy[50_000]
    tuple_index = time.perf_counter() - start
    print(f"Create list: {list_create:.6f}s | create tuple: {tuple_create:.6f}s")
    print(f"Index list:  {list_index:.8f}s | index tuple:  {tuple_index:.8f}s")

    try:
        stops[[13.0418, 80.2341]] = "Not allowed"
    except TypeError as error:
        print("List as dictionary key:", type(error).__name__, "-", error)

    print("\nTuples are useful for fixed records and hashable keys.")
    print("A shallow copy duplicates the outer container; deep copy duplicates nested objects.")


if __name__ == "__main__":
    main()
