def test_filter_all_exceed():
    tasks = [{'title': 'Task A', 'effort_h': 10.0}, {'title': 'Task B', 'effort_h': 7.5}]
    assert filter_urgent_tasks(tasks, 5.0) == []