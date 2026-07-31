class MatchResult:
    def __init__(self, employee, project, match_percentage, status, missing_skills=None):
        self.employee = employee
        self.project = project
        self.match_percentage = match_percentage
        self.status = status
        self.missing_skills = missing_skills if missing_skills is not None else []

    def __repr__(self):
        missing_str = f" | Missing Skills: {', '.join(self.missing_skills)}" if self.missing_skills else ""
        return (
            f"Project: {self.project.proj_name} | Employee: {self.employee.name} | "
            f"Match: {self.match_percentage:.2f}% | Status: {self.status}{missing_str}"
        )


def parse_skills(skills_str):
    """Helper method to parse comma-separated skills into a set of clean, lowercased strings."""
    if not skills_str:
        return set()
    return {skill.strip().lower() for skill in skills_str.split(',') if skill.strip()}


def evaluate_matches(employees, projects):
    """
    Compares each open project's required skills against each bench employee's skills,
    computes match percentages, and classifies the pairing.
    """
    match_results = []

    for project in projects:
        req_skills = parse_skills(project.required_skills)
        
        # Skip if the project has no required skills defined to avoid division by zero
        if not req_skills:
            continue

        for employee in employees:
            emp_skills = parse_skills(employee.skills)

            # Compute intersection and missing skills
            matching_skills = req_skills.intersection(emp_skills)
            missing_skills_set = req_skills.difference(emp_skills)
            
            # Calculate match percentage based on required skills
            match_percentage = (len(matching_skills) / len(req_skills)) * 100

            # Classify based on percentage thresholds
            if match_percentage >= 80:
                status = "Full Match"
                missing = []
            elif 50 <= match_percentage < 80:
                status = "Needs Minimal Upskilling"
                # Keep original case/formatting for display if available, else use set values
                missing = list(missing_skills_set)
            else:
                status = "Not Suitable"
                missing = []

            # Store the result object
            result = MatchResult(
                employee=employee,
                project=project,
                match_percentage=match_percentage,
                status=status,
                missing_skills=missing
            )
            match_results.append(result)

    return match_results