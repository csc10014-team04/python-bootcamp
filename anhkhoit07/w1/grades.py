# Write summary(scores: list[float]) -> dict returning {"min", "max", "mean", "median"}. 
# Round mean and median to 2 decimals. An empty list raises ValueError.
# e.g.: summary([7.5, 9, 6, 8])

# def summary(list) -> dict
def summary(scores: list[float]) -> dict:
    if not scores:
        raise ValueError("empty list") # raise error for empty list
    
    scores.sort()
    n = len(scores)
    mean_val = round(sum(scores) / n, 2)
    
    if n % 2 == 0:
        median_val = round((scores[n // 2 - 1] + scores[n // 2]) / 2, 2)
    else:
        median_val = round(scores[n // 2], 2)
        
    return {
        "min": scores[0],
        "max": scores[-1],
        "mean": mean_val,
        "median": median_val
    }