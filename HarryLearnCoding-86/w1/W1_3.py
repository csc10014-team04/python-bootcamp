"""Week 1 Task 3: Thesis registration eligibility check."""


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Determine whether student meets thesis registration criteria.

    Args:
        credits: Total earned academic credits.
        gpa: Cumulative Grade Point Average.

    Returns:
        True if credits >= 120 and gpa >= 2.0, False otherwise.
    """
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """List unsatisfied requirements for thesis registration.

    Args:
        credits: Total earned academic credits.
        gpa: Cumulative Grade Point Average.

    Returns:
        List of missing requirement descriptions.
    """
    reasons: list[str] = []

    if credits < 120:
        reasons.append(f"need {120 - credits} more credits")

    if gpa < 2.0:
        reasons.append(f"need {round(2.0 - gpa, 2)} higher gpa")

    return reasons
