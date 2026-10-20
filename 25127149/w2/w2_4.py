import pytest
import math

def is_task_eligible(score: float, threshold: float = 70.0, inclusive: bool = True) -> bool:

    if inclusive:
        return score >= threshold
    return score > threshold

def test_exact_match_inclusive():
    assert is_task_eligible(score=70.0, threshold=70.0, inclusive=True) is True

def test_exact_match_exclusive():
    
    assert is_task_eligible(score=70.0, threshold=70.0, inclusive=False) is False

def test_just_below_threshold_inclusive():
    assert is_task_eligible(score=69.999, threshold=70.0, inclusive=True) is False

def test_just_above_threshold_exclusive():
    assert is_task_eligible(score=70.001, threshold=70.0, inclusive=False) is True

def test_zero_threshold_boundary():
    assert is_task_eligible(score=0.0, threshold=0.0, inclusive=True) is True
    assert is_task_eligible(score=0.0, threshold=0.0, inclusive=False) is False



def test_floating_point_imprecision_boundary():
    accumulated_score = 69.1 + 0.9  # Kết quả tính toán thực tế xấp xỉ 70.00000000000001
    threshold = 70.0
    
    assert is_task_eligible(score=accumulated_score, threshold=threshold, inclusive=True) is True
