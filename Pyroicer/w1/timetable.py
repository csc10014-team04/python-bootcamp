def by_day(course_list):
    result = {}
    
    for course, day in course_list:
        result.setdefault(day, []).append(course)
        
    for day in result:
        result[day].sort()
        
    return result