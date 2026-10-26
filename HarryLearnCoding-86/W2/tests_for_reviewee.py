"""W2-4: Cross-testing a teammate's W1 functions."""

import pytest

from w1.grades import summary
from w1.rules import can_register_thesis, missing
from w1.text_tools import top_k, word_count
from w1.timetable import by_day


def test_summary_even_length() -> None:
    """Test summary with an even number of elements to verify median calculation."""
    res = summary([7.5, 9.0, 6.0, 8.0])
    assert res == {"min": 6.0, "max": 9.0, "mean": 7.62, "median": 7.75}


def test_summary_empty_raises_value_error() -> None:
    """Edge case: empty list must raise ValueError."""
    with pytest.raises(ValueError):
        summary([])


def test_word_count_and_top_k_ties() -> None:
    """Test word count punctuation removal and alphabetical tie-breaking in top_k."""
    text = "Git is fun. Git is fast!"
    assert word_count(text) == {"git": 2, "is": 2, "fun": 1, "fast": 1}
    # Both 'git' and 'is' have count 2, 'fast' and 'fun' have count 1
    assert top_k(text, 2) == [("git", 2), ("is", 2)]


def test_thesis_boundary_cases() -> None:
    """Test exact threshold boundary values for credits and gpa."""
    assert can_register_thesis(120, 2.0) is True
    assert can_register_thesis(119, 2.0) is False
    assert can_register_thesis(120, 1.99) is False
    assert missing(118, 1.85) == ["need 2 more credits", "need 0.15 higher gpa"]


def test_by_day_duplicate_days_sorted() -> None:
    """Edge case: multiple courses on the same day must be sorted alphabetically."""
    schedule = [
        ("CSC10014", "Mon"),
        ("MTH00003", "Tue"),
        ("CSC10001", "Mon"),
        ("ENG00001", "Mon"),
    ]
    result = by_day(schedule)
    assert result["Mon"] == ["CSC10001", "CSC10014", "ENG00001"]
    assert result["Tue"] == ["MTH00003"]
