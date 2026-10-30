"""Test task eligibility threshold behavior."""

def is_task_eligible(
    score: float,
    threshold: float = 70.0,
    inclusive: bool = True,
) -> bool:
    """Return whether score meets the threshold under the chosen boundary rule."""
    if inclusive:
        return score >= threshold
    return score > threshold


def test_exact_match_inclusive() -> None:
    """An exact threshold match qualifies when inclusive."""
    assert is_task_eligible(score=70.0, threshold=70.0, inclusive=True) is True


def test_exact_match_exclusive() -> None:
    """An exact threshold match does not qualify when exclusive."""
    assert is_task_eligible(score=70.0, threshold=70.0, inclusive=False) is False


def test_just_below_threshold_inclusive() -> None:
    """A score below the threshold does not qualify."""
    assert is_task_eligible(score=69.999, threshold=70.0, inclusive=True) is False


def test_just_above_threshold_exclusive() -> None:
    """A score above the threshold qualifies when exclusive."""
    assert is_task_eligible(score=70.001, threshold=70.0, inclusive=False) is True


def test_zero_threshold_boundary() -> None:
    """Check inclusive and exclusive comparisons at zero."""
    assert is_task_eligible(score=0.0, threshold=0.0, inclusive=True) is True
    assert is_task_eligible(score=0.0, threshold=0.0, inclusive=False) is False


def test_floating_point_imprecision_boundary() -> None:
    """Check a floating-point value that is marginally above the threshold."""
    accumulated_score = 69.1 + 0.9
    threshold = 70.0
    assert (
        is_task_eligible(
            score=accumulated_score,
            threshold=threshold,
            inclusive=True,
        )
        is True
    )
