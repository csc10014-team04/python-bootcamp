def can_register_thesis(credits: int, gpa: float) -> bool:
    if credits >= 120 and gpa >= 2.0:
        return True

def missing(credits: int, gpa: float) -> list[str]:
    reasons = []
    
    if credits < 120:
        short = 120 - credits
        plural = "" 
        if short != 1:
            plural="s"
        reasons.append(f"need {short} more credit{plural}")
        
    if gpa < 2.0:
        reasons.append("need higher GPA (>=2.0)")
        
    return reasons