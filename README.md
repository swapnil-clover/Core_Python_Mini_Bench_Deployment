# Mini Bench Deployment System
### Intelligent Skill-Based Matching for Bench Employees and Open Projects

---

## Executive Summary

The **Mini Bench Deployment System** is a lightweight, dependency-free Python CLI tool that helps organizations redeploy idle talent faster. It automatically evaluates every employee currently "on the bench" against every open project opportunity, scoring each pairing on skill compatibility.

Beyond matching, the system quantifies **bench-ageing risk**, giving managers a clear signal on which employees require urgent redeployment. The result is a console dashboard and exportable CSV report that transforms a manual, spreadsheet-driven process into a fast, repeatable, data-backed workflow.

Built entirely on the Python standard library, the tool requires no external services, databases, or installation steps — making it easy to run, audit, and extend in any environment.

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [System Workflow](#system-workflow)
- [Matching Engine](#matching-engine)
- [Bench Ageing Analysis](#bench-ageing-analysis)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Input File Formats](#input-file-formats)
- [Sample Output](#sample-output)
- [Future Enhancements](#future-enhancements)

---

## Overview

Bench management is a persistent challenge in project-driven organizations. Employees between assignments represent both a cost center and an underused resource, while open projects frequently struggle to identify suitably skilled candidates in time. The Mini Bench Deployment System addresses this by automating the matching process end-to-end — from data ingestion to prioritized, actionable reporting.

## Problem Statement

Organizations that manage a rotating pool of bench employees typically face:

- **Manual matching overhead** — HR and PMO teams cross-reference spreadsheets by hand to identify suitable candidates for open roles.
- **Delayed redeployment** — Employees remain idle longer than necessary, increasing cost and disengagement risk.
- **Invisible upskilling opportunities** — Employees actively learning a required skill are easily overlooked in manual reviews.
- **Lack of prioritization** — Without a consistent ageing metric, at-risk (long-idle) employees don't get the attention they need.

## Solution

The system solves these challenges through a fully automated, four-stage pipeline:

1. **Ingest** — Load bench employee and open project data from CSV.
2. **Analyze** — Calculate bench duration and assign an ageing-risk flag per employee.
3. **Match** — Score every employee against every open project based on current and in-progress skills.
4. **Report** — Present results via a console dashboard, a bench-ageing report, and a CSV export.

---

## Features

| Feature | Description |
|---|---|
| **Skill Matching** | Scores every employee against every open project based on required skill overlap. |
| **Weighted Scoring** | Awards partial credit for skills an employee is actively learning, without inflating final classification. |
| **Bench Analysis** | Calculates exact days-on-bench for each employee from their bench start date. |
| **Ageing Priority** | Flags employees as Normal, Attention, High Priority, or Critical based on bench duration. |
| **Missing Skills Insight** | Identifies the exact skill gaps standing between an employee and a full match. |
| **Full Combination Reporting** | Preserves every employee–project pairing rather than showing only a single "best match." |
| **CSV Export** | Generates a complete, structured report for offline analysis or sharing. |
| **Resilient Data Loading** | Skips malformed CSV rows with a warning instead of failing the entire run. |

---

## System Workflow

```text
                     +----------------------+
                     |   employees.csv      |
                     |  open_projects.csv   |
                     |  total_employees.txt |
                     +----------------------+
                                |
                                v
                     +----------------------+
                     |  data_handler.py     |
                     |  Load & Model Data   |
                     +----------------------+
                                |
         +----------------------+----------------------+
         |                                              |
         v                                              v
+----------------------+                    +----------------------+
|    analytics.py       |                    |     matcher.py        |
|  Bench-Ageing Logic   |                    |   Skill-Match Engine  |
+----------------------+                    +----------------------+
         |                                              |
         +----------------------+----------------------+
                                |
                                v
                     +----------------------+
                     |     report.py         |
                     | Dashboard + CSV Export|
                     +----------------------+
```

---

## Matching Engine

Each employee–project pair is evaluated using two independent scores:

| Metric | Description |
|---|---|
| **Current Match %** | Percentage of required skills the employee *already possesses*. This is the sole driver of classification. |
| **Weighted Score** | Adds partial credit (0.6× weight) for skills the employee is *currently learning*. Used only as a sorting tiebreaker — it never affects classification. |
| **Missing Skills** | Required skills the employee has not yet acquired, forming a ready-made upskilling plan. |

**Classification Tiers**

| Tier | Threshold |
|---|---|
| 🟢 Full Match | Current match ≥ 80% |
| 🟡 Needs Minimal Upskilling | Current match 50–79% |
| 🔴 Not Suitable | Current match < 50% |

Every employee is compared against **every** open project — no results are discarded in favor of a single "best fit," ensuring managers retain full visibility into all viable deployment options.

---

## Bench Ageing Analysis

Bench duration is calculated from each employee's bench start date and mapped to a priority flag:

| Days on Bench | Flag |
|---|---|
| 0–30 | Normal |
| 31–60 | Attention |
| 61–90 | High Priority |
| 90+ | Critical — Immediate Deployment Needed |

---

## Project Structure

```text
├── main.py              # Orchestrates the pipeline: load → analyze → match → report
├── data_handler.py      # Employee / Project data models and CSV loaders
├── analytics.py         # Bench-duration calculation and ageing flags
├── matcher.py           # Skill-matching engine (MatchResult + evaluate_matches)
├── report.py            # Console dashboard, ageing report, and CSV export
├── data/
│   ├── employees.csv        # Input: bench employee data
│   ├── open_projects.csv    # Input: open project requirements
│   └── total_employees.txt  # Input: total company headcount
└── output/
    └── bench_report.csv     # Output: generated after running main.py
```

---

## Getting Started

**Requirements:** Python 3.8+ — no third-party dependencies (standard library only: `csv`, `datetime`).

```bash
python3 main.py
```

Running the script will:

- Print the number of bench employees and total company headcount loaded
- Print the overall bench percentage
- Print the full employee × project match dashboard
- Print the bench-ageing report (sorted by days on bench, descending)
- Write the complete match report to `output/bench_report.csv`

---

## Input File Formats

**`employees.csv`**

| Column | Description |
|---|---|
| EmployeeID | Unique identifier, e.g. `E147` |
| Name | Employee full name |
| Skills | Comma-separated list of skills the employee currently holds |
| Experience | Years of experience (integer) |
| BenchSince | Date the employee entered the bench, `YYYY-MM-DD` |
| LearningSkills | Comma-separated list of skills currently in progress |

**`open_projects.csv`**

| Column | Description |
|---|---|
| ProjectID | Unique identifier, e.g. `P501` |
| ProjectName | Project name |
| RequiredSkills | Comma-separated list of skills required by the project |
| PositionsOpen | Number of open positions (integer) |

**`total_employees.txt`** — a single integer representing total company headcount, used to compute the overall bench percentage.

---

## Sample Output

```text
EmployeeID  EmployeeName    DaysOnBench  BenchFlag   Project                     MatchPct  WeightedScore  Status
E189        Meera Chauhan   3            Normal      Full Stack Web Application  83.33     93.33          Full Match
E189        Meera Chauhan   3            Normal      Data Science Analytics...   16.67     16.67          Not Suitable
E114        Pooja Kulkarni  36           Attention   Mobile App Development      83.33     83.33          Full Match
```

The console output is complemented by a bench-ageing report (sorted oldest-first) and a complete `bench_report.csv` export covering every employee-project pairing.

---

## Future Enhancements

- Interactive web dashboard (Flask or Streamlit) as an alternative to console output
- Automated Slack/email alerts for Critical-flagged employees
- Historical trend tracking of bench percentage over time
- Configurable skill-matching thresholds and weighting
