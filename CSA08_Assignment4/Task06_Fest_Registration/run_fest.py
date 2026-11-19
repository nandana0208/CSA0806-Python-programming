from pathlib import Path
from fest_registration.processor import process_folder

def main():
    here = Path(__file__).parent
    result = process_folder(here / "input", here / "output")
    print("TASK 6 - COLLEGE FEST")
    for key, value in result.items():
        print(f"{key.replace('_',' ').title()}: {value}")
    print("Output files:", ", ".join(sorted(p.name for p in (here / "output").iterdir())))
if __name__ == "__main__":
    main()
