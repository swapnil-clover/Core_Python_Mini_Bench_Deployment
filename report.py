import csv

# Column widths for the console dashboard. Each width is sized to fit the
# longest value that can actually appear in that column, with NO internal
# padding budget — the visible gap between columns is added separately as a
# 2-space literal (GAP) so the spacing is explicit, not baked into .ljust().
COL_WIDTHS = {
    "EmployeeID": 4,       # longest: "E200"
    "EmployeeName": 16,    # longest: "Vishal Deshmukh"
    "DaysOnBench": 3,      # longest: "177"
    "BenchFlag": 38,       # longest: "Critical - Immediate Deployment needed"
    "Project": 31,         # longest: "Cloud Infrastructure Automation"
    "MatchPct": 6,         # longest: "100.00"
    "WeightedScore": 6,    # longest: "100.00"
    "Status": 25,          # longest: "Needs Minimal Upskilling"
    "MissingSkills": 20,   # longest: "data science; pandas"
}

# Visible gap (in spaces) inserted between every pair of adjacent columns.
GAP = "  "

# Fieldnames for the bench_report.csv export — kept in sync with COL_WIDTHS order.
CSV_FIELDNAMES = [
    "EmployeeID",
    "EmployeeName",
    "DaysOnBench",
    "BenchFlag",
    "Project",
    "MatchPct",
    "WeightedScore",
    "Status",
    "MissingSkills",
]


def _rows_for_employee(employee, match_results):
    """Return ALL MatchResult rows for an employee — one dict per employee/project pair.

    CHANGE: this replaces the old `_best_match_for_employee`, which sorted an
    employee's matches and kept only the top-scoring one. Every employee-project
    combination is now preserved and returned as its own row.

    Rows are still sorted (current_pct desc, then weighted_score desc as a
    tiebreaker) purely so the highest matches for an employee appear first in
    the dashboard/CSV — this is a display ordering choice only, it does not
    discard any rows the way the old code did.

    If an employee has no match_results at all (e.g. every project was skipped
    by the matcher for having no parsable required skills), a single
    placeholder row is returned so the employee still appears in the report.
    """
    emp_results = [r for r in match_results if r.employee is employee]

    days = getattr(employee, "days_on_bench", 0)
    flag = getattr(employee, "flag", "Normal")

    if not emp_results:
        return [{
            "EmployeeID": employee.emp_id,
            "EmployeeName": employee.name,
            "DaysOnBench": days,
            "BenchFlag": flag,
            "Project": "-",
            "MatchPct": 0.0,
            "WeightedScore": 0.0,
            "Status": "Not Suitable",
            "MissingSkills": "",
        }]

    emp_results = sorted(
        emp_results,
        key=lambda r: (r.current_pct, r.weighted_score),
        reverse=True,
    )

    rows = []
    for result in emp_results:
        # Semicolon-join missing skills so commas don't collide with CSV quoting.
        missing = "; ".join(result.missing_skills) if result.missing_skills else ""
        rows.append({
            "EmployeeID": employee.emp_id,
            "EmployeeName": employee.name,
            "DaysOnBench": days,
            "BenchFlag": flag,
            "Project": result.project.proj_name,
            "MatchPct": round(result.current_pct, 2),
            "WeightedScore": round(result.weighted_score, 2),
            "Status": result.status,
            "MissingSkills": missing,
        })
    return rows


def print_dashboard(match_results, employees):
    """Print a console dashboard showing EVERY employee/project match pair.

    CHANGE: previously this printed exactly one line per employee (their best
    match only). It now prints one line per employee-project combination, so
    an employee with 3 open projects produces 3 lines.

    Uses f-strings + .ljust() for text columns and .rjust() for numeric columns,
    with an explicit 2-space gap (GAP) between every pair of adjacent columns.
    Each column width is sized to fit the longest possible value for that column.
    """
    print()
    print("=" * 170)
    print("BENCH DEPLOYMENT - EMPLOYEE / PROJECT DASHBOARD (all combinations)")
    print("=" * 170)

    header = (
        f"{'EmployeeID'.ljust(COL_WIDTHS['EmployeeID'])}{GAP}"
        f"{'EmployeeName'.ljust(COL_WIDTHS['EmployeeName'])}{GAP}"
        f"{'DaysOnBench'.rjust(COL_WIDTHS['DaysOnBench'])}{GAP}"
        f"{'BenchFlag'.ljust(COL_WIDTHS['BenchFlag'])}{GAP}"
        f"{'Project'.ljust(COL_WIDTHS['Project'])}{GAP}"
        f"{'MatchPct'.rjust(COL_WIDTHS['MatchPct'])}{GAP}"
        f"{'WeightedScore'.rjust(COL_WIDTHS['WeightedScore'])}{GAP}"
        f"{'Status'.ljust(COL_WIDTHS['Status'])}{GAP}"
        f"{'MissingSkills'.ljust(COL_WIDTHS['MissingSkills'])}"
    )
    print(header)
    print("-" * 170)

    for employee in employees:
        rows = _rows_for_employee(employee, match_results)
        for row in rows:
            match_pct_str = f"{row['MatchPct']:.2f}"
            weighted_str = f"{row['WeightedScore']:.2f}"
            line = (
                f"{str(row['EmployeeID']).ljust(COL_WIDTHS['EmployeeID'])}{GAP}"
                f"{str(row['EmployeeName']).ljust(COL_WIDTHS['EmployeeName'])}{GAP}"
                f"{str(row['DaysOnBench']).rjust(COL_WIDTHS['DaysOnBench'])}{GAP}"
                f"{str(row['BenchFlag']).ljust(COL_WIDTHS['BenchFlag'])}{GAP}"
                f"{str(row['Project']).ljust(COL_WIDTHS['Project'])}{GAP}"
                f"{match_pct_str.rjust(COL_WIDTHS['MatchPct'])}{GAP}"
                f"{weighted_str.rjust(COL_WIDTHS['WeightedScore'])}{GAP}"
                f"{str(row['Status']).ljust(COL_WIDTHS['Status'])}{GAP}"
                f"{str(row['MissingSkills']).ljust(COL_WIDTHS['MissingSkills'])}"
            )
            print(line)
        print("-" * 170)


def print_bench_ageing(employees):
    """Print the bench-ageing report sorted by days_on_bench descending.

    UNCHANGED — this report is per-employee by nature (bench ageing has
    nothing to do with project matches) and was not touched.

    Uses sorted() + a lambda key as required by the spec.
    Column widths match print_dashboard() and add the same explicit 2-space
    gap (GAP) between every pair of adjacent columns.
    """
    ageing_widths = {
        "EmployeeID": COL_WIDTHS["EmployeeID"],
        "EmployeeName": COL_WIDTHS["EmployeeName"],
        "DaysOnBench": COL_WIDTHS["DaysOnBench"],
        "BenchFlag": COL_WIDTHS["BenchFlag"],
    }

    print()
    print("=" * 75)
    print("BENCH AGEING REPORT (sorted by days on bench, descending)")
    print("=" * 75)

    header = (
        f"{'EmployeeID'.ljust(ageing_widths['EmployeeID'])}{GAP}"
        f"{'EmployeeName'.ljust(ageing_widths['EmployeeName'])}{GAP}"
        f"{'DaysOnBench'.rjust(ageing_widths['DaysOnBench'])}{GAP}"
        f"{'BenchFlag'.ljust(ageing_widths['BenchFlag'])}"
    )
    print(header)
    print("-" * 75)

    ageing_sorted = sorted(employees, key=lambda e: e.days_on_bench, reverse=True)
    for employee in ageing_sorted:
        days = getattr(employee, "days_on_bench", 0)
        flag = getattr(employee, "flag", "Normal")
        line = (
            f"{str(employee.emp_id).ljust(ageing_widths['EmployeeID'])}{GAP}{GAP}{GAP}{GAP}"
            f"{str(employee.name).ljust(ageing_widths['EmployeeName'])}{GAP}"
            f"{str(days).rjust(ageing_widths['DaysOnBench'])}{GAP}{GAP}{GAP}{GAP}{GAP}"
            f"{str(flag).ljust(ageing_widths['BenchFlag'])}"
        )
        print(line)
    print("-" * 75)


def export_bench_report(match_results, employees, filename="bench_report.csv"):
    """Export EVERY employee-project match row to filename using csv.DictWriter.

    CHANGE: previously wrote exactly one row per employee (their best match).
    Now writes one row per employee-project combination, so the CSV row count
    equals the number of (bench employee) x (open project) pairs evaluated
    (plus one placeholder row per employee with zero evaluable projects).

    Fieldnames mirror the dashboard columns. File writing is wrapped in
    try/except OSError so a non-writable path produces a clear message
    instead of a traceback.
    """
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()
            for employee in employees:
                for row in _rows_for_employee(employee, match_results):
                    writer.writerow(row)
        print(f"\nBench report exported to '{filename}'.")
    except OSError as e:
        print(f"\nError: could not write bench report to '{filename}': {e}")
