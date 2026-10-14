def by_day(courses):
    res={}
    for course,day in courses:
        res.setdefault(day,[]).append(course)
    for day in res:
        res[day].sort()
    return res