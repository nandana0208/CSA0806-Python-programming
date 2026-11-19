# CSA08 – Assignment 5 (CO5)
## Data Acquisition, Cleaning, Analysis and AI Applications

**Student name:** [Enter your name]  
**Register number:** [Enter your register number]  
**Python version used to prepare this project:** Python 3.x

This project follows the supplied Assignment 5 brief and the City Air-Quality Monitoring Network case study. Replace the student details above before submission.

## Folder guide
- `Task01_Data_Acquisition/` – CSV structure, data-quality inspection, SQLite schema and CSV-vs-SQL discussion.
- `Task02_Cleaning_Normalisation/` – cleaning rules, min-max scaling and z-score standardisation.
- `Task03_Analysis_Visualisation/` – chart selection and summary-table design.
- `Task04_Debugging_Profiling/` – debugging and profiling plan.
- `Task05_AI_Complaints/` – lexicon sentiment, extractive summary and rule-based chatbot design.
- `Task06_Integrated_Pipeline/` – runnable Python implementation, sample data, database, charts, outputs and screenshots.

## Setup and run
```bash
python -m pip install -r requirements.txt
python Task06_Integrated_Pipeline/main.py
```

The program creates a cleaned CSV, SQLite database, daily summaries, chart images and a text report in `Task06_Integrated_Pipeline/output/`.

## Task results
1. Data acquisition: station CSV columns are read and mapped into normalised station and reading tables.
2. Cleaning: blank/NA readings are treated as missing, invalid sensor values are removed, duplicate observations are removed, and Fahrenheit values are converted to Celsius.
3. Analysis: SQL produces daily summaries; matplotlib creates monthly trend, station comparison, temperature-vs-PM2.5 and hourly distribution charts.
4. Debugging/profiling: assertions validate important invariants and `perf_counter`/`cProfile` capture execution behaviour.
5. AI application: a simple negation-aware lexicon scorer, extractive summariser and keyword-driven chatbot are demonstrated.

**Important:** The screenshots are sample outputs produced by executing this project in the preparation environment. Run the programs on your own computer, inspect the results, and capture your own screenshots before submitting. Add your own measurements and interpretations where required by your instructor.
