# Task 7 – Build a Module

`import milkrate` exposes functions as `milkrate.payout`; `from milkrate import payout` imports the function name directly; `import milkrate as mr` provides a short alias. `if __name__ == "__main__":` runs the demonstration only when the file is executed directly. On import, `__name__` is the module name (`milkrate`), so the demonstration table is not printed.

Python searches locations in `sys.path`, including the script's directory and installed library directories. `decimal` is a standard-library module. A shared module avoids copying rate formulas into multiple scripts; a rate revision is made once. Import has a one-time loading cost and Python caches imported modules in `sys.modules`. Reusing the module is O(1) function lookup plus calculation; the import cost is amortised over subsequent calls.
