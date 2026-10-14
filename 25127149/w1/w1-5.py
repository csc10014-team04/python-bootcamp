def by_day(items: list[tuple[str, str]]) -> dict[str, list[str]]:
    result = {}

    for course, day in items:
        result.setdefault(day, []).append(course)

    for day in result:
        result[day].sort()

    return result

