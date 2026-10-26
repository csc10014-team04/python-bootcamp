"""Week 1 Task 5: Timetable grouping by day."""


def by_day(timetable: list[tuple[str, str]]) -> dict[str, list[str]]:
    """Group courses by day of week with alphabetically sorted course lists.

    Args:
        timetable: List of (course_code, day_name) tuples.

    Returns:
        Mapping from day name to sorted list of course codes.
    """
    grouped: dict[str, list[str]] = {}
    for course, day in timetable:
        grouped.setdefault(day, []).append(course)

    return {day: sorted(courses) for day, courses in grouped.items()}
