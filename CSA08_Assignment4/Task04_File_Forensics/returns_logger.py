"""Show file logging defects and repair them with append mode and context managers."""
from pathlib import Path
import tempfile

def faulty_save(books, log_path):
    log = open(log_path, "w", encoding="utf-8")
    for book in books:
        log.write(book)       # No newline: records are joined.
    log.close()

def faulty_process(day_file, log_path):
    try:
        books = open(day_file, encoding="utf-8").read().split("\\n")
        faulty_save(books, log_path)  # "w" erases previous days.
    except FileNotFoundError:
        print("missing")

def save_returns(books, log_path):
    with open(log_path, "a", encoding="utf-8") as log:
        for book in books:
            if book.strip():
                log.write(book.strip() + "\\n")

def process(day_file, log_path, error_log):
    try:
        with open(day_file, "r", encoding="utf-8") as source:
            books = [line.strip() for line in source if line.strip()]
        save_returns(books, log_path)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as error:
        with open(error_log, "a", encoding="utf-8") as log:
            log.write(f"{day_file}: {type(error).__name__}: {error}\\n")
        print(f"Could not process {day_file}: {error}")

def main():
    with tempfile.TemporaryDirectory() as temp:
        folder = Path(temp)
        days = []
        for i, titles in enumerate((["Book A", "Book B"], ["Book C"], ["Book D"]), 1):
            path = folder / f"day{i}.txt"
            path.write_text("\\n".join(titles) + "\\n", encoding="utf-8")
            days.append(path)
        bad_log = folder / "faulty.log"
        for day in days:
            faulty_process(day, bad_log)
        print("TASK 4 - FILE FORENSICS")
        print("Faulty log:", repr(bad_log.read_text(encoding="utf-8")))
        good, errors = folder / "returns.log", folder / "errors.log"
        for day in days:
            process(day, good, errors)
        process(folder / "missing.txt", good, errors)
        print("Repaired log:")
        print(good.read_text(encoding="utf-8"), end="")
        print("Error log:", errors.read_text(encoding="utf-8").strip())

if __name__ == "__main__":
    main()
