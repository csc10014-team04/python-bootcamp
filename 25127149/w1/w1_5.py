"""Group course names by day."""


def by_day(items: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group courses by day and sort course names within each day."""
    result: dict[str, list[str]] = {}
    for course, day in items:
        result.setdefault(day, []).append(course)

    for courses in result.values():
        courses.sort()
    return result
