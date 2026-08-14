import csv


COL_WIDTHS = {
    "EmployeeID": 4,       
    "EmployeeName": 16,   
    "DaysOnBench": 3,    
    "BenchFlag": 38,       
    "Project": 31,         
    "MatchPct": 6,         
    "WeightedScore": 6,    
    "Status": 25,          
    "MissingSkills": 20,   
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
    # return sorted(rows, key=lambda x: getattr(x.employee, "DaysOnBench", 0))
    return sorted(rows, key=lambda x: x["DaysOnBench"])


def print_dashboard(match_results, employees):
    """Print a console dashboard showing EVERY employee/project match pair.
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


def export_bench_report(match_results, employees, filename="output/bench_report.csv"):
    """Export EVERY employee-project match row to filename using csv.DictWriter.
    Fieldnames mirror the dashboard columns. File writing is wrapped in
    try/except OSError so a non-writable path produces a clear message
    instead of a traceback.
    """
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)
            writer.writeheader()

            # Sort employees by days on bench descending
            sorted_employees = sorted(employees, key=lambda e: getattr(e, "days_on_bench", 0), reverse=True)
            for employee in sorted_employees:
                for row in _rows_for_employee(employee, match_results):
                    writer.writerow(row)
        print(f"\nBench report exported to '{filename}'.")
    except OSError as e:
        print(f"\nError: could not write bench report to '{filename}': {e}")
