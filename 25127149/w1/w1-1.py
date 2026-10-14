from statistics import median
def summary(scores: list[float]) -> dict:
    if not scores:
        raise ValueError("scores cannot be empty")
    return {
        "min" : min(scores),
        "max" : max(scores),
        "mean": round(sum(scores) / len(scores), 2),
        "median": round(median(scores), 2)
        }
