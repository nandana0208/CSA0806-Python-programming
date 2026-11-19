"""Run four equivalent examples of organising an attendance utility."""
from pathlib import Path
import subprocess, sys

def main():
    root = Path(__file__).parent
    print("TASK 5 - FOUR MODULE ORGANISATIONS")
    for folder, script in [("A_one_script", "attendance.py"),
                           ("B_one_module", "main.py"),
                           ("C_three_modules", "main.py"),
                           ("D_package", "main.py")]:
        result = subprocess.run([sys.executable, str(root / folder / script)],
                                cwd=root / folder, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
        print(f"\\n[{folder}]\\n{result.stdout.strip()}")
    print("\\nPackage organisation separates reading, statistics and reporting.")
if __name__ == "__main__":
    main()
