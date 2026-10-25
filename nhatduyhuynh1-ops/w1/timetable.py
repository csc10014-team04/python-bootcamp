def by_day(courses):
    res={}
    for course,day in courses:
        res.setdefault(day,[]).append(course)
    for day,value in res.items():
        value.sort()
    return res