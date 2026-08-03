import analytics
import data_handler
import matcher
import report


def main():
    # 1. Load all input data.
    employees = data_handler.load_employees("employees.csv")
    projects = data_handler.load_projects("open_projects.csv")
    total_employees = data_handler.load_total_employees("total_employees.txt")

    if not employees or not projects:
        print("Cannot proceed: employee or project data failed to load.")
        return

    # 2. Run bench analytics — attach days_on_bench and flag to each employee.
    bench = analytics.Analytics(employees, total_employees)
    bench.Calculate_bench_days()
    bench_pct = bench.overall_bench_percentage()
    print(f"Loaded {len(employees)} bench employees.")
    print(f"Total company headcount: {total_employees}.")
    print(f"Overall bench percentage: {bench_pct:.2f}%.")

    # 3. Run skill matching.
    match_results = matcher.evaluate_matches(employees, projects)
    print(f"Computed {len(match_results)} employee/project match pairs.")

    # 4. Reporting — console dashboard + bench-ageing + CSV export.
    report.print_dashboard(match_results, employees)
    report.print_bench_ageing(employees)
    report.export_bench_report(match_results, employees, "bench_report.csv")


if __name__ == "__main__":
    main()