import csv


class Employee:
    def __init__(self, emp_id, name, skills, experience, bench_since, learning_skills):
        self.emp_id = emp_id
        self.name = name
        self.skills = skills
        self.experience = experience
        self.bench_since = bench_since
        self.learning_skills = learning_skills

    def __repr__(self):
        return (
            f"EmpID: {self.emp_id} | Name: {self.name} | "
            f"Skills: {self.skills} | Experience: {self.experience} | "
            f"Bench Since: {self.bench_since} | Learning Skills: {self.learning_skills}"
        )


class Project:
    def __init__(self, proj_id, proj_name, required_skills, positions_open):
        self.proj_id = proj_id
        self.proj_name = proj_name
        self.required_skills = required_skills
        self.positions_open = positions_open

    def __repr__(self):
        return (
            f"ProjectID: {self.proj_id} | ProjectName: {self.proj_name} | "
            f"RequiredSkills: {self.required_skills} | "
            f"PositionsOpen: {self.positions_open}"
        )


def load_employees(filename="output/employees.csv"):
    """Read employees.csv with csv.DictReader. Skills / LearningSkills columns may
    contain quoted comma-separated strings; csv.DictReader handles that natively.
    Rows that are missing required fields or fail to parse are skipped with a warning.
    """
    employees_data = []
    required_fields = ("EmployeeID", "Name", "Skills", "Experience", "BenchSince", "LearningSkills")
    try:
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    if any(row.get(f) is None for f in required_fields):
                        raise ValueError(f"Missing one of {required_fields}")
                    employee_obj = Employee(
                        row["EmployeeID"],
                        row["Name"],
                        row["Skills"],
                        row["Experience"],
                        row["BenchSince"],
                        row["LearningSkills"],
                    )
                    employees_data.append(employee_obj)
                except (KeyError, ValueError, IndexError) as e:
                    print(f"Warning: skipping malformed employee row {row}: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
    return employees_data


def load_projects(filename="data/open_projects.csv"):
    """Read open_projects.csv with csv.DictReader. positions_open is cast to int
    so callers can do arithmetic on it without a TypeError.
    Malformed rows are skipped with a warning rather than crashing the whole load.
    """
    projects_data = []
    required_fields = ("ProjectID", "ProjectName", "RequiredSkills", "PositionsOpen")
    try:
        with open(filename, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    if any(row.get(f) is None for f in required_fields):
                        raise ValueError(f"Missing one of {required_fields}")
                    project_obj = Project(
                        row["ProjectID"],
                        row["ProjectName"],
                        row["RequiredSkills"],
                        int(row["PositionsOpen"]),
                    )
                    projects_data.append(project_obj)
                except (KeyError, ValueError, IndexError) as e:
                    print(f"Warning: skipping malformed project row {row}: {e}")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
    return projects_data


def load_total_employees(filename="data/total_employees.txt"):
    """Read total_employees.txt and return its contents as an int.
    The file is expected to contain a single integer (e.g.'700'), possibly
    surrounded by whitespace.
    """
    try:
        with open(filename, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
        return 0
    except ValueError as e:
        print(f"Error: Could not parse headcount from '{filename}': {e}")
        return 0 