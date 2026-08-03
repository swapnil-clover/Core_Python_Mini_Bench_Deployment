from datetime import date, datetime

class InvalidBenchDateError(Exception):
    """Raised when an employee's BenchSince value cannot be parsed as a date."""


class Analytics:
    def __init__(self, bench_employees, total_employees):
        self.bench_employees = bench_employees
        self.total_employees = total_employees

    def Calculate_bench_days(self):
        for employee in self.bench_employees:
            # Parse bench_since string (e.g., "2026-05-15") to a date object
            if isinstance(employee.bench_since, str):
                try:
                    bench_since_date = datetime.strptime(employee.bench_since, "%Y-%m-%d").date()
                except ValueError:
                    raise InvalidBenchDateError(
                        f"Invalid BenchSince date for employee {employee.name} "
                        f"(ID {employee.emp_id}): {employee.bench_since!r}"
                    )
            else:
                bench_since_date = employee.bench_since

            employee.days_on_bench = (date.today() - bench_since_date).days

            if employee.days_on_bench > 90:
                employee.flag = "Critical - Immediate Deployment needed"
            elif employee.days_on_bench > 60:
                employee.flag = "High Priority"
            elif employee.days_on_bench > 30:
                employee.flag = "Attention"
            else:
                employee.flag = "Normal"

    def overall_bench_percentage(self):
        if len(self.bench_employees) == 0:
            return 0
        return (len(self.bench_employees) / self.total_employees) * 100
