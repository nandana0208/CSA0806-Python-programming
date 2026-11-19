from pathlib import Path
def read_department_file(path):
    with Path(path).open("r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            yield line_no, line.rstrip("\\n")
