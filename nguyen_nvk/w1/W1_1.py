def summary(scores: list[float]) -> dict:
    if not scores:
        raise ValueError("Scores must not be empty")
    
    a = sorted(scores)
    n = len(a)
    
    if n % 2 == 0:
        median = (a[n // 2] + a[n // 2 - 1]) / 2.0
    else:
        median = float(a[n // 2])
        
    return {
        'min': a[0], 
        'max': a[-1], 
        'mean': round(sum(a) / n, 2), 
        'median': round(median, 2)
    }
