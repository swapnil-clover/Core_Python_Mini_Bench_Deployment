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
    Evaluates matches between employees and projects.
    - Current Skills have a higher weight (e.g., 1.0).
    - Learning Skills have a slightly lesser weight (e.g., 0.6) to reflect potential rather than mastery.
    """
    match_results = []

    # Weight configurations
    CURRENT_SKILL_WEIGHT = 1.0
    LEARNING_SKILL_WEIGHT = 0.6  # Slightly less weight for learning skills

    for project in projects:
        req_skills = parse_skills(project.required_skills)
        
        if not req_skills:
            continue

        for employee in employees:
            emp_skills = parse_skills(employee.skills)
            learning_skills = parse_skills(employee.learning_skills)

            # Find matching current skills and matching learning skills against requirements
            matched_current = req_skills.intersection(emp_skills)
            matched_learning = req_skills.intersection(learning_skills)

            # Prevent double-counting if a skill is present in both current and learning
            matched_learning = matched_learning.difference(matched_current)

            # Calculate total weighted score
            score = (len(matched_current) * CURRENT_SKILL_WEIGHT) + (len(matched_learning) * LEARNING_SKILL_WEIGHT)

            # Calculate final match percentage relative to total required skills
            match_percentage = (score / len(req_skills)) * 100

            # Determine true missing skills (not present in current or learning)
            total_covered = matched_current.union(matched_learning)
            missing_skills_set = req_skills.difference(total_covered)

            # Define status thresholds based on the adjusted percentage
            if match_percentage >= 80:
                status = "Full Match"
                missing = []
            elif 50 <= match_percentage < 80:
                status = "Needs Minimal Upskilling"
                missing = list(missing_skills_set)
            else:
                status = "Not Suitable"
                missing = list(missing_skills_set)

            # Create and store result object
            result = MatchResult(
                employee=employee,
                project=project,
                match_percentage=match_percentage,
                status=status,
                missing_skills=missing
            )
            match_results.append(result)

    return match_results