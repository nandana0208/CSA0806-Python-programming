"""Q6 - A nested dictionary timetable with a station lookup index."""

import random
import time
from collections import defaultdict

TIMETABLE = {
    "12601": {
        "name": "Chennai Mail",
        "stops": [
            ("Chennai", "06:00", "06:10"),
            ("Arakkonam", "07:20", "07:22"),
            ("Katpadi", "08:30", "08:35"),
        ],
        "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat"},
    },
    "12602": {
        "name": "Coimbatore Express",
        "stops": [
            ("Chennai", "07:00", "07:15"),
            ("Katpadi", "09:10", "09:15"),
            ("Salem", "11:00", "11:05"),
        ],
        "days": {"Mon", "Wed", "Fri", "Sun"},
    },
    "12603": {
        "name": "Nilgiri Passenger",
        "stops": [
            ("Chennai", "08:00", "08:10"),
            ("Arakkonam", "09:30", "09:32"),
            ("Salem", "12:00", "12:05"),
        ],
        "days": {"Tue", "Thu", "Sat"},
    },
    "12604": {
        "name": "Bengaluru Intercity",
        "stops": [
            ("Chennai", "09:00", "09:10"),
            ("Katpadi", "11:00", "11:05"),
            ("Bengaluru", "13:00", "13:05"),
        ],
        "days": {"Mon", "Tue", "Wed", "Thu", "Fri"},
    },
    "12605": {
        "name": "Coastal Link",
        "stops": [
            ("Chennai", "10:00", "10:10"),
            ("Arakkonam", "11:30", "11:32"),
            ("Salem", "14:00", "14:05"),
        ],
        "days": {"Sat", "Sun"},
    },
}


def build_station_index(timetable):
    index = defaultdict(list)
    for train_number, details in timetable.items():
        for station, arrival, departure in details["stops"]:
            index[station].append((train_number, arrival, departure))
    return dict(index)


def find_trains(timetable, station, day):
    matches = []
    for number, details in timetable.items():
        if day in details["days"]:
            for stop in details["stops"]:
                if stop[0].lower() == station.lower():
                    matches.append((number, details["name"], stop[2]))
    return sorted(matches, key=lambda item: item[2])


def main():
    index = build_station_index(TIMETABLE)
    print("Q6 - RAILWAY TIMETABLE")
    print("Trains stopping at Chennai on Monday:")
    for number, name, departure in find_trains(TIMETABLE, "Chennai", "Mon"):
        print(f"{number} | {name:<22} | departure {departure}")

    print("\nStation index keys:", sorted(index))
    print("Unknown station:", index.get("Nowhere", []))
    print("Third stop departure for train 12601:", TIMETABLE["12601"]["stops"][2][2])

    print("\nNeat timetable:")
    for number, details in TIMETABLE.items():
        print(f"{number} - {details['name']} ({', '.join(sorted(details['days']))})")
        for station, arrival, departure in details["stops"]:
            print(f"    {station:<12} arrives {arrival}, leaves {departure}")

    # A small experiment compares scanning every stop with using the index.
    print("\nQuery timing (synthetic timetable):")
    for train_count in (100, 1_000, 10_000):
        large = {}
        for number in range(train_count):
            large[str(number)] = {
                "name": f"Train {number}",
                "stops": [(f"Station{i % 100}", "08:00", "08:05")
                          for i in range(8)],
                "days": {"Mon", "Wed"},
            }
        start = time.perf_counter()
        scan = find_trains(large, "Station25", "Mon")
        scan_time = time.perf_counter() - start
        start = time.perf_counter()
        large_index = build_station_index(large)
        indexed = [item for item in large_index.get("Station25", [])]
        index_time = time.perf_counter() - start
        assert len(scan) == len(indexed)
        print(f"{train_count:>5} trains | scan query {scan_time:.6f}s | "
              f"build index + retrieve {index_time:.6f}s")

    print("\nThe index makes repeated station queries faster, but needs extra memory and update work.")


if __name__ == "__main__":
    main()
