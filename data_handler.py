# view_bench_data.py

try:
    with open("employees.csv", "r") as file:
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
        
            print(f"EmpID: {emp_id} | Name: {name} | Skills: {skills} | Bench Days: {bench_days}")

except FileNotFoundError:
    print("Error: The file 'employees.csv' does not exist.")

with open("open_projects.csv", "r") as file:
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
            
        print(f"ProjectID: {proj_id} | ProjectName: {proj_name} | RequiredSkills: {skills} | PositionsOpen: {positions_open}")