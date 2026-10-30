"""Check whether a student can register for a thesis."""


def can_register_thesis(credits: int, gpa: float) -> bool:
    """Return whether the credit and GPA requirements are both satisfied."""
    return credits >= 120 and gpa >= 2.0


def missing(credits: int, gpa: float) -> list[str]:
    """Return human-readable reasons the student cannot register."""
    reasons: list[str] = []
    if credits < 120:
        reasons.append(f"need {120 - credits} more credits")
    if gpa < 2.0:
        reasons.append(f"need GPA of at least 2.0 (current: {gpa})")
    return reasons


def main() -> None:
    """Print thesis registration eligibility examples."""
    examples = [(118, 2.5), (125, 1.8), (125, 3.0)]
    for credits, gpa in examples:
        print(can_register_thesis(credits, gpa))
        print(missing(credits, gpa))


if __name__ == "__main__":
    main()
