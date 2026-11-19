"""Q3 - Count and group farmer helpline complaints with dictionaries."""

import random
import re
import string
import time
from collections import Counter, defaultdict

CALLS = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]
STOP_WORDS = {"not", "high", "the", "is", "a", "and"}


def words_in(text):
    """Lowercase text and keep alphabetic words only."""
    return re.findall(r"[a-z]+", text.lower())


def frequencies(texts, stop):
    counts = {}
    for text in texts:
        for word in words_in(text):
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts


def top(counts, k):
    """Sort by descending count, then alphabetically for ties."""
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]


def group_by_district(records):
    grouped = defaultdict(list)
    for record in records:
        grouped[record["district"]].append(record["complaint"])
    return dict(grouped)


def benchmark(count):
    vocabulary = ["seed", "water", "crop", "price", "loan", "pest", "fertiliser"]
    generated = [
        " ".join(random.choices(vocabulary, k=12))
        for _ in range(count)
    ]
    start = time.perf_counter()
    result = frequencies(generated, set())
    dictionary_time = time.perf_counter() - start

    all_words = [word for line in generated for word in words_in(line)]
    distinct = set(all_words)
    start = time.perf_counter()
    slow_result = {word: all_words.count(word) for word in distinct}
    list_count_time = time.perf_counter() - start

    start = time.perf_counter()
    counter_result = Counter(all_words)
    counter_time = time.perf_counter() - start
    assert result == slow_result == dict(counter_result)
    return dictionary_time, list_count_time, counter_time


def main():
    print("Q3 - FARMER HELPLINE COMPLAINTS")
    counts = frequencies(CALLS, STOP_WORDS)
    print("Word counts:", counts)
    print("Top 3 words:", top(counts, 3))

    records = [
        {"district": "Kanchipuram", "crop": "rice", "complaint": "seed not received"},
        {"district": "Tiruvallur", "crop": "maize", "complaint": "pest attack"},
        {"district": "Kanchipuram", "crop": "rice", "complaint": "water shortage"},
    ]
    print("Complaints by district:", group_by_district(records))

    print("\nTiming comparison (seconds; generated sample data):")
    for size in (1_000, 10_000, 100_000):
        dictionary_time, list_time, counter_time = benchmark(size)
        print(f"{size:>6} complaints | dict {dictionary_time:.5f} | "
              f"list.count {list_time:.5f} | Counter {counter_time:.5f}")

    print("\nEdge checks:")
    print("Empty text:", frequencies([""], STOP_WORDS))
    print("Mixed case/punctuation:", frequencies(["SEEDS, seeds! Not received."], STOP_WORDS))
    print("Dictionary keys preserve insertion order in Python 3.7+.")
    print("Expected time: dictionary and Counter O(n) average; repeated list.count O(n*d).")


if __name__ == "__main__":
    main()
