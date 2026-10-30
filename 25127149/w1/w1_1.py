"""Summarize a collection of numeric scores."""

from statistics import median


def summary(scores: list[float]) -> dict[str, float]:
    """Return the minimum, maximum, mean, and median of scores.

    Raises:
        ValueError: If scores is empty.
    """
    if not scores:
        raise ValueError("scores cannot be empty")
    return {
        "min": min(scores),
        "max": max(scores),
        "mean": round(sum(scores) / len(scores), 2),
        "median": round(median(scores), 2),
    }
