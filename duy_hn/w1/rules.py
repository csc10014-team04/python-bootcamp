def can_register_thesis(credits: int, gpa: float) -> bool:
    return credits >= 120 and gpa >= 2


def missing(credits, gpa) -> list[str]:
    res=[]
    if credits <120:
        res.append(f"need {120 - credits} more credits")
    if gpa <2:
        res.append(f"need {2-gpa} more gpa")
    return res
