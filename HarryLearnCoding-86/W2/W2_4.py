import pytest

def filter_urgent_tasks(tasks: list[dict], threshold: float) -> list[dict]:
    if threshold < 0:
        raise ValueError("Threshold cannot be negative")
    return [t for t in tasks if t['effort'] <= threshold]

def test_filter_baseline():
    tasks = [{'title': 'A', 'effort': 2}, {'title': 'B', 'effort_h': 5}]
    assert len(filter_urgent_tasks(tasks, 3)) == 1

def test_filter_empty_list():
    assert filter_urgent_tasks([], 5) == []

def test_filter_all_exceed():
    tasks = [{'title': 'A', 'effort': 10}]
    assert filter_urgent_tasks(tasks, 5) == []

def test_filter_exact_boundary():
    tasks = [{'title': 'A', 'effort': 5}]
    assert len(filter_urgent_tasks(tasks, 5)) == 1

def test_filter_missing_keys():
    tasks = [{'title': 'A'}]
    with pytest.raises(KeyError):
        filter_urgent_tasks(tasks, 5)

def test_filter_negative_threshold():
    tasks = [{'title': 'A', 'effort': 2}]
    with pytest.raises(ValueError, match="Threshold cannot be negative"):
        filter_urgent_tasks(tasks, -1)