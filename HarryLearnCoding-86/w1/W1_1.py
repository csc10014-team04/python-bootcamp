"""Week 1 Task 1: Grade summary calculation."""


def summary(scores: list[float]) -> dict[str, float]:
    """Calculate min, max, mean, and median from a list of scores.

    Args:
        scores: Non-empty list of numerical scores.

    Returns:
        Dictionary with 'min', 'max', 'mean', and 'median' rounded to 2 decimals.

    Raises:
        ValueError: If scores list is empty.
    """
    if not scores:
        raise ValueError("Scores must not be empty")

    a = sorted(scores)
    n = len(a)

    if n % 2 == 0:
        median = (a[n // 2] + a[n // 2 - 1]) / 2.0
    else:
        median = float(a[n // 2])

    return {
        "min": float(a[0]),
        "max": float(a[-1]),
        "mean": round(sum(a) / n, 2),
        "median": round(median, 2),
    }
