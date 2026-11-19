"""Q1 - Daily rainfall records: lists, slicing and moving averages."""

import random
import time


def weekly_totals(readings):
    """Return the total rainfall for each complete or partial week."""
    return [sum(readings[start:start + 7]) for start in range(0, len(readings), 7)]


def moving_average_naive(readings, window=7):
    """Calculate each average by adding the whole window again."""
    if window <= 0:
        raise ValueError("window must be positive")
    return [
        sum(readings[start:start + window]) / window
        for start in range(len(readings) - window + 1)
    ]


def moving_average_running(readings, window=7):
    """Calculate averages by updating one running total."""
    if window <= 0:
        raise ValueError("window must be positive")
    if len(readings) < window:
        return []

    total = sum(readings[:window])
    averages = [total / window]

    for end in range(window, len(readings)):
        total += readings[end] - readings[end - window]
        averages.append(total / window)

    return averages


def benchmark(size):
    readings = [random.randint(0, 40) for _ in range(size)]
    start = time.perf_counter()
    naive = moving_average_naive(readings)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    running = moving_average_running(readings)
    running_time = time.perf_counter() - start

    assert naive == running
    return naive_time, running_time


def main():
    random.seed(8)
    readings = [random.randint(0, 40) for _ in range(365)]

    weeks = weekly_totals(readings)
    wettest = max(enumerate(weeks, start=1), key=lambda item: item[1])
    driest = min(enumerate(weeks, start=1), key=lambda item: item[1])
    dry_days = [day for day, amount in enumerate(readings, start=1) if amount == 0]

    print("Q1 - DAILY RAINFALL")
    print("Readings recorded:", len(readings))
    print("First three weekly totals:", weeks[:3])
    print(f"Wettest week: {wettest[0]} ({wettest[1]} mm)")
    print(f"Driest week:  {driest[0]} ({driest[1]} mm)")
    print("7-day moving averages (first 5):",
          [round(value, 2) for value in moving_average_running(readings)[:5]])
    print("Dry days (first 10):", dry_days[:10])
    print("Slice readings[7:14]:", readings[7:14])
    print("Slice readings[-7:]:", readings[-7:])
    print("Slice readings[::7] (every seventh item):", readings[::7][:8])

    print("\nMoving-average timing (seconds)")
    for size in (365, 36_500, 365_000):
        naive_time, running_time = benchmark(size)
        print(f"{size:>7} readings | naive {naive_time:.6f} | running {running_time:.6f}")

    print("\nShort-input checks:")
    print("Empty list:", moving_average_running([]))
    print("Fewer than 7 readings:", moving_average_running([2, 4, 6]))

    # For a window of 7, the naive method adds 7 values for each output:
    # 7 * (n - 6) additions. The running-sum method uses about n additions.
    print("\nComplexity: naive O(7n) = O(n); running sum O(n), with less repeated work.")
    print("List insert is O(n) in the worst case because later items shift.")


if __name__ == "__main__":
    main()
