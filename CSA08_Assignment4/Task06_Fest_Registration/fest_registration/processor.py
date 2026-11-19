from pathlib import Path
import csv
from .reader import read_department_file
from .validator import InvalidRegistration, parse_registration

def process_folder(input_folder, output_folder):
    source, output = Path(input_folder), Path(output_folder)
    output.mkdir(parents=True, exist_ok=True)
    master, seen, errors = {}, set(), []
    duplicates = missing = 0
    files = sorted(source.glob("*.txt"))
    if not files:
        errors.append(("INPUT", 0, "no department files found", ""))
    for path in files:
        try:
            for line_no, raw in read_department_file(path):
                try:
                    record = parse_registration(raw)
                    reg = record["register"]
                    if reg in seen:
                        duplicates += 1
                        master[reg]["events"].update(record["events"])
                        master[reg]["emails"].add(record["email"])
                    else:
                        seen.add(reg)
                        master[reg] = {**record, "emails": {record["email"]}}
                except InvalidRegistration as error:
                    errors.append((path.name, line_no, str(error), raw))
        except FileNotFoundError as error:
            missing += 1
            errors.append((path.name, 0, f"missing file: {error}", ""))
        except (PermissionError, UnicodeDecodeError, OSError) as error:
            errors.append((path.name, 0, f"{type(error).__name__}: {error}", ""))
    with (output / "master_list.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Register", "Name", "Department", "Emails", "Events"])
        for reg, item in sorted(master.items()):
            writer.writerow([reg, item["name"], item["department"],
                ";".join(sorted(item["emails"])), ";".join(sorted(item["events"]))])
    event_groups = {}
    for reg, item in master.items():
        for event in item["events"]:
            event_groups.setdefault(event, []).append((reg, item["name"], item["department"]))
    for event, participants in event_groups.items():
        safe = "".join(c.lower() if c.isalnum() else "_" for c in event).strip("_")
        with (output / f"event_{safe}.csv").open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Register", "Name", "Department"])
            writer.writerows(sorted(participants))
    with (output / "summary.txt").open("w", encoding="utf-8") as file:
        file.write(f"Unique registrations: {len(master)}\\nDuplicates merged: {duplicates}\\n")
        file.write(f"Rejected rows: {len(errors)}\\nMissing files: {missing}\\nEvents: {len(event_groups)}\\n")
    with (output / "error_log.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["File", "Line", "Reason", "Original"])
        writer.writerows(errors)
    return {"accepted": len(master), "duplicates": duplicates,
            "rejected": len(errors), "missing_files": missing}
