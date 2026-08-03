class MatchResult:
    def __init__(self,employee,project,match_percentage,status,missing_skills=None,current_pct=0.0,weighted_score=0.0):
        self.employee = employee
        self.project = project
        self.match_percentage = match_percentage  # legacy alias for current_pct
        self.current_pct = current_pct
        self.weighted_score = weighted_score
        self.status = status
        self.missing_skills = missing_skills if missing_skills is not None else []

    def __repr__(self):
        missing_str = f" | Missing Skills: {', '.join(self.missing_skills)}" if self.missing_skills else ""
        return (
            f"Project: {self.project.proj_name} | Employee: {self.employee.name} | "
            f"Match: {self.current_pct:.2f}% (weighted {self.weighted_score:.2f}%) | "
            f"Status: {self.status}{missing_str}"
        )


def parse_skills(skills_str):
    """Helper: parse a comma-separated skills string into a set of clean lowercased tokens."""
    if not skills_str:
        return set()
    return {skill.strip().lower() for skill in skills_str.split(',') if skill.strip()}


def evaluate_matches(employees, projects):
    """Evaluate matches between employees and projects.

    Two separate scores are computed per (employee, project) pair:
      - current_pct    : unweighted % using ONLY matched_current (skills the employee
                         actually knows). This drives the Full Match / Needs Minimal
                         Upskilling / Not Suitable classification. Learning skills
                         cannot promote an employee into a higher tier.
      - weighted_score : the existing weighted % that gives learning skills partial
                         credit (weight 0.6 vs 1.0 for known skills). This is kept
                         as a tiebreaker for sorting within a tier and for
                         reporting visibility — it is never used to set the status label.
    """
    match_results = []

    # Weight configurations
    CURRENT_SKILL_WEIGHT = 1.0
    LEARNING_SKILL_WEIGHT = 0.6

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

            current_count = len(matched_current)
            learning_count = len(matched_learning)
            total_required = len(req_skills)

            # Unweighted current-skill match — drives classification
            current_pct = (current_count / total_required) * 100

            # Weighted score (kept for tiebreaking / reporting only)
            score = (current_count * CURRENT_SKILL_WEIGHT) + (learning_count * LEARNING_SKILL_WEIGHT)
            weighted_score = (score / total_required) * 100

            # True missing skills = required skills not in the employee's known skill set.
            # Learning skills do NOT cover gaps for the purpose of this list — the
            # employee hasn't actually mastered them yet.
            missing_skills_set = req_skills.difference(matched_current)

            # Classification runs on the UNWEIGHTED current_pct — this is the fix
            # for the bug where learning skills could falsely promote an employee
            # to "Full Match".
            if current_pct >= 80:
                status = "Full Match"
                missing = []
            elif 50 <= current_pct < 80:
                status = "Needs Minimal Upskilling"
                missing = list(missing_skills_set)
            else:
                status = "Not Suitable"
                missing = list(missing_skills_set)

            result = MatchResult(
                employee=employee,
                project=project,
                match_percentage=current_pct,  # legacy field, mirrors current_pct
                current_pct=current_pct,
                weighted_score=weighted_score,
                status=status,
                missing_skills=missing,
            )
            match_results.append(result)

    return match_results