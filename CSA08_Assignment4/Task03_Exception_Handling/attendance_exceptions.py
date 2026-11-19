"""Custom exception and complete try/except/else/finally example."""
import os
import tempfile

class InvalidRecord(Exception):
    """Attendance row is not in the required format."""

def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    register, date, status = (part.strip() for part in parts)
    if not register or not date:
        raise InvalidRecord("register number and date must not be empty")
    if status not in {"P", "A"}:
        raise InvalidRecord(f"invalid status {status!r}")
    return register, date, status

def summarise(path):
    present, absent, errors = 0, 0, []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                try:
                    register, date, status = parse_line(line)
                except InvalidRecord as error:
                    errors.append((line_no, str(error)))
                else:
                    if status == "P":
                        present += 1
                    else:
                        absent += 1
    except FileNotFoundError as error:
        raise FileNotFoundError(f"attendance file not found: {path}") from error
    except PermissionError as error:
        raise PermissionError(f"cannot read attendance file: {path}") from error
    except UnicodeDecodeError as error:
        raise ValueError(f"file is not UTF-8: {path}") from error
    finally:
        # with closes a successfully opened file, even if an exception occurs.
        pass
    return present, absent, errors

def main():
    data = ("192311001,2026-10-08,P\\n192311002,2026-10-08,A\\n"
            "192311003,2026-10-08\\n192311004,2026-10-08,L\\n")
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(data)
        name = tmp.name
    try:
        print("TASK 3 - EXCEPTION HANDLING")
        print("Expected result:", summarise(name))
        try:
            summarise(name + ".missing")
        except FileNotFoundError as error:
            print("Missing-file test:", error)
    finally:
        os.remove(name)

if __name__ == "__main__":
    main()
