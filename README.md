# Mini Bench Deployment System

A lightweight Python tool that matches employees currently on the "bench"
(unassigned to a project) against open project openings based on skills,
and reports bench-ageing risk so managers can prioritize deployment.

## What it does

1. Loads bench employees and open projects from CSV.
2. Calculates how long each employee has been on the bench and flags
   ageing risk (Normal / Attention / High Priority / Critical).
3. Compares **every employee against every open project** and scores
   each pairing on skill match.
4. Classifies each employee-project pair as:
   - **Full Match** — current skill match ≥ 80%
   - **Needs Minimal Upskilling** — current skill match 50–79%
   - **Not Suitable** — current skill match < 50%
5. Prints a console dashboard, a bench-ageing report, and exports a CSV
   with every employee-project combination (not just the best one).

## Project structure

```
.
├── main.py              # Orchestrates the pipeline: load → analyze → match → report
├── data_handler.py      # Employee / Project classes + CSV loaders
├── analytics.py         # Bench-days calculation, ageing flags, bench %
├── matcher.py           # Skill-matching engine — MatchResult + evaluate_matches()
├── report.py            # Console dashboard, ageing report, CSV export
├── employees.csv        # Input: bench employee data
├── open_projects.csv    # Input: open project requirements
├── total_employees.txt  # Input: total company headcount (single integer)
└── bench_report.csv     # Output: generated after running main.py
```

## Requirements

- Python 3.8+
- No third-party packages — standard library only (`csv`, `datetime`)

## Running it

```bash
python3 main.py
```

This will:
- Print how many bench employees and total headcount were loaded
- Print overall bench percentage
- Print the full employee × project match dashboard to the console
- Print the bench-ageing report (sorted by days on bench, descending)
- Write `bench_report.csv` in the current directory

## Input file formats

**`employees.csv`**

| Column         | Description                                              |
|----------------|-----------------------------------------------------------|
| EmployeeID     | Unique ID, e.g. `E147`                                     |
| Name           | Employee full name                                         |
| Skills         | Comma-separated list of skills the employee currently has |
| Experience     | Years of experience (integer)                               |
| BenchSince     | Date employee went on bench, `YYYY-MM-DD`                  |
| LearningSkills | Comma-separated skills the employee is currently learning  |

**`open_projects.csv`**

| Column         | Description                                    |
|----------------|-------------------------------------------------|
| ProjectID      | Unique ID, e.g. `P501`                          |
| ProjectName    | Project name                                    |
| RequiredSkills | Comma-separated list of skills the project needs |
| PositionsOpen  | Number of open positions (integer)              |

**`total_employees.txt`** — a single integer, the total company headcount
(used to compute overall bench percentage).

## Matching logic

For each employee-project pair, `matcher.py` computes:

- **`current_pct`** — percentage of the project's required skills the
  employee *already knows*. This is the only score used for
  classification — learning skills can never promote an employee into
  a higher tier.
- **`weighted_score`** — a secondary score that gives partial credit
  (0.6x weight) for skills the employee is currently learning. Shown in
  reports for context and used only as a tiebreaker when sorting, never
  for classification.
- **`missing_skills`** — required skills the employee doesn't currently
  know (regardless of tier), useful for identifying upskilling paths.

Every employee-project combination is preserved in the output — the
system does not pick a single "best" project per employee. An employee
strong in mobile development will simply show up as "Not Suitable" for
the cloud infrastructure project, and "Full Match" for the mobile
project, in the same report.

## Sample dashboard output

```
EmployeeID  EmployeeName    DaysOnBench  BenchFlag   Project                     MatchPct  WeightedScore  Status                     MissingSkills
E114        Pooja Kulkarni  36           Attention   Mobile App Development      83.33     83.33          Full Match
E114        Pooja Kulkarni  36           Attention   Data Science Analytics...   0.00      0.00           Not Suitable               machine learning; numpy; ...
E114        Pooja Kulkarni  36           Attention   Cloud Infrastructure...     0.00      10.00           Not Suitable               terraform; docker; linux; ...
```

## Bench ageing flags

| Days on bench | Flag                                    |
|----------------|------------------------------------------|
| 0–30           | Normal                                    |
| 31–60          | Attention                                 |
| 61–90          | High Priority                             |
| 90+            | Critical - Immediate Deployment needed    |

## Notes

- Malformed CSV rows are skipped with a warning rather than crashing
  the whole load.
- If `bench_report.csv` can't be written (e.g. permissions issue), the
  error is caught and reported instead of raising a traceback.
