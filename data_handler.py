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
                
                # Simple line parsing while accounting for quoted skill strings
                if '"' in line:
                    parts = line.split('"')
                    before_quotes = parts[0].rstrip(',').split(',')
                    skills = parts[1]
                    after_quotes = parts[2].lstrip(',').split(',')
                    
                    emp_id = before_quotes[0]
                    name = before_quotes[1]
                    bench_days = after_quotes[0]
                else:
                    parts = line.split(',')
                    emp_id = parts[0]
                    name = parts[1]
                    skills = parts[2]
                    bench_days = parts[3]
            
                formatted_emp = f"EmpID: {emp_id} | Name: {name} | Skills: {skills} | Bench Days: {bench_days}"
                employees_data.append(formatted_emp)

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
                    
                formatted_proj = f"ProjectID: {proj_id} | ProjectName: {proj_name} | RequiredSkills: {skills} | PositionsOpen: {positions_open}"
                projects_data.append(formatted_proj)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")

    return projects_data
