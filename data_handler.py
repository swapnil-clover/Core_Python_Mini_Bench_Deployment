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


def load_employees(filename="employees.csv"):
    employees_data = []
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            
            # Skip header line (index 0) and iterate through records
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                
                # Parsing structure expecting both Skills and LearningSkills to be quoted:
                # Format: emp_id, name, "skills", experience, bench_since, "learning_skills"
                parts = line.split('"')
                
                # parts[0] -> emp_id, name, (e.g., "E101,Vikram Singh,")
                before_skills = parts[0].rstrip(',').split(',')
                emp_id = before_skills[0]
                name = before_skills[1]
                
                # parts[1] -> skills inside the first set of quotes
                skills = parts[1]
                
                # parts[2] -> middle unquoted values (experience, bench_since), e.g., ",3,2026-05-15,"
                middle_values = parts[2].strip(',').split(',')
                experience = middle_values[0]
                bench_since = middle_values[1]
                
                # parts[3] -> learning_skills inside the second set of quotes
                learning_skills = parts[3]
            
                # Create an Employee object and append to the list
                employee_obj = Employee(emp_id, name, skills, experience, bench_since, learning_skills)
                employees_data.append(employee_obj)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")

    return employees_data


def load_projects(filename="open_projects.csv"):
    projects_data = []
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                
                # Simple line parsing while accounting for quoted skill strings
                if '"' in line:
                    parts = line.split('"')
                    before_quotes = parts[0].rstrip(',').split(',')
                    skills = parts[1]
                    after_quotes = parts[2].lstrip(',').split(',')
                    
                    proj_id = before_quotes[0]
                    proj_name = before_quotes[1]
                    positions_open = after_quotes[0]

                else:
                    parts = line.split(',')
                    proj_id = parts[0]
                    proj_name = parts[1]
                    skills = parts[2]
                    positions_open = parts[3]
                    
                # Create a Project object and append to the list
                project_obj = Project(proj_id, proj_name, skills, positions_open)
                projects_data.append(project_obj)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")

    return projects_data
