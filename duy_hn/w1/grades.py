def summary(scores: list[float]) -> dict:
    if not scores:
        raise ValueError("scores cant be empty")
    sort=sorted(scores)
    n=len(scores)
    mid=n//2
    if n%2==0:
        median=(sort[mid-1]+sort[mid])/2
    else:
        median=sort[mid]
    return {"min": min(scores),"max": max(scores),"median": median,"mean": sum(scores)/n}