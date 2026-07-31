from datetime import date

class Analytics:
    def __init__(self,bench_employees,total_employees) -> None:
        self.bench_employees = bench_employees
        self.total_employees = total_employees

    def Calculate_bench_days(self):
        for employee in self.bench_employees:
            employee.days_on_bench = (date.today() - employee.bench_since).days

            if employee.days_on_bench > 90:
                employee.flag = "Critical - Immediate Deployement needed"
            elif employee.days_on_bench > 60:
                employee.flag = "High Priority"
            elif employee.days_on_bench > 30:
                employee.flag = "Attention"
            else:
                employee.flag = "Normal"

    def overall_bench_percentage(self):
        if len(self.bench_employees == 0):
            return 0
        return(len(self.bench_employees)/len(self.total_employees)*100)