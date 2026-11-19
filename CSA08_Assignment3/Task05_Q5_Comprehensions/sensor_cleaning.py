"""Q5 - Clean cold-storage readings and convert temperature units."""

import random
import sys
import time


def clean_with_loop(readings):
    celsius, fahrenheit = [], []
    for value in readings:
        if -50 <= value <= 50:
            celsius.append(value)
            fahrenheit.append(value * 9 / 5 + 32)
    return celsius, fahrenheit


def clean_with_comprehension(readings):
    celsius = [value for value in readings if -50 <= value <= 50]
    fahrenheit = [value * 9 / 5 + 32 for value in readings if -50 <= value <= 50]
    return celsius, fahrenheit


def clean_with_map_filter(readings):
    valid = filter(lambda value: -50 <= value <= 50, readings)
    celsius = list(valid)
    fahrenheit = list(map(lambda value: value * 9 / 5 + 32, celsius))
    return celsius, fahrenheit


def benchmark(size):
    readings = [random.uniform(-60, 60) for _ in range(size)]
    results = []
    for function in (clean_with_loop, clean_with_comprehension, clean_with_map_filter):
        start = time.perf_counter()
        result = function(readings)
        results.append((time.perf_counter() - start, result))
    assert results[0][1] == results[1][1] == results[2][1]
    return [item[0] for item in results]


def main():
    readings = [4.5, 7.2, 55.0, -60.0, 1.5, 9.0, 6.0, 51.0]
    celsius, fahrenheit = clean_with_loop(readings)
    alarms = [
        (minute, value)
        for minute, value in enumerate(readings, start=1)
        if not 2 <= value <= 8
    ]

    print("Q5 - SENSOR READING CLEANUP")
    print("Original readings:", readings)
    print("Valid Celsius:", celsius)
    print("Converted Fahrenheit:", [round(value, 2) for value in fahrenheit])
    print("Alarm minutes (minute, temperature):", alarms)

    loop_result = clean_with_loop(readings)
    comp_result = clean_with_comprehension(readings)
    map_result = clean_with_map_filter(readings)
    print("All three methods agree:", loop_result == comp_result == map_result)

    print("\nTiming comparison (seconds):")
    for size in (10_000, 100_000, 1_000_000):
        timings = benchmark(size)
        print(f"{size:>9}: loop {timings[0]:.5f} | "
              f"comprehension {timings[1]:.5f} | map/filter {timings[2]:.5f}")

    generator = (value for value in readings if -50 <= value <= 50)
    valid_list = [value for value in readings if -50 <= value <= 50]
    print("\nContainer size only (bytes): list =", sys.getsizeof(valid_list),
          "| generator =", sys.getsizeof(generator))
    print("All-valid test:", clean_with_comprehension([1, 2, 3])[0])
    print("All-invalid test:", clean_with_comprehension([99, -99])[0])
    print("A list comprehension uses O(n) result memory; a generator is lazy and uses O(1) extra space.")


if __name__ == "__main__":
    main()
