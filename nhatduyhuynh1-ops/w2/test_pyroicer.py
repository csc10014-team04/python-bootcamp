
import pytest

from Pyroicer.w1.grades import summary
from Pyroicer.w1.rules import can_register_thesis, missing
from Pyroicer.w1.text_tools import top_k, word_count
from Pyroicer.w1.timetable import by_day


def test_summary_normal():
    assert summary([7.5, 9, 6, 8]) == {
        "min": 6,
        "max": 9,
        "mean": 7.62,
        "median": 7.75
    }


def test_summary_empty():
    with pytest.raises(ValueError):
        summary([])


def test_word_count_case_and_punctuation():
    assert word_count("Git, git! Python; PYTHON.") == {
        "git": 2,
        "python": 2
    }


def test_top_k_count_then_alphabetical():
    assert top_k("banana apple cherry", 2) == [
        ("apple", 1),
        ("banana", 1)
    ]


def test_thesis_exact_eligibility_boundary():
    assert can_register_thesis(120, 2.0) is True


def test_thesis_one_credit_below_boundary():
    assert can_register_thesis(119, 2.0) is False


def test_missing_credits():
    assert "need 2 more credits" in missing(118, 3.0)


def test_by_day_groups_and_sorts():
    assert by_day([
        ("CSC10014", "Mon"),
        ("MTH00003", "Tue"),
        ("CSC10001", "Mon")
    ]) == {
        "Mon": ["CSC10001", "CSC10014"],
        "Tue": ["MTH00003"]
    }
