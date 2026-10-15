def summary(scores: list[float]) -> dict:
    
    if not scores:
        raise ValueError("Scores must not be empty!")

    ordered = sorted(scores)
    n = len(ordered)

    mean = round(sum(ordered) / n, 2)

    if n % 2 == 1:
        median = float(ordered[n // 2])
    else:
        median = (ordered[n // 2 - 1] + ordered[n // 2]) / 2

    median = round(median, 2)

    return {
        "min": min(scores),
        "max": max(scores),
        "mean": mean,
        "median": median
    }
