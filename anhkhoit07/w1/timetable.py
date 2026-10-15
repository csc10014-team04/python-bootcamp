def by_day(schedule: list[tuple[str, str]]) -> dict[str, list[str]]:
    result = {}
    for course, day in schedule:
        result.setdefault(day, []).append(course) # group courses by day
    for day in result:
        result[day].sort() # sort course lists alphabetically
    return result