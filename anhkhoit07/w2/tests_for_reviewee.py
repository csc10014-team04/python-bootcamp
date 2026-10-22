import pytest
from datetime import date
from models import Task
from errors import InfeasiblePlan, check_feasible


def filter_tasks_by_threshold(tasks: list[dict], threshold_h: float) -> list[dict]:
    return [task for task in tasks if task["effort_h"] < threshold_h] # sample filter implementation


def test_empty_input_array_assigned_to_khoi():
    empty_list = []
    result = filter_tasks_by_threshold(empty_list, 5.0) # process empty list
    assert result == [] # verify empty return without iteration errors


def test_empty_task_objects_processing():
    tasks = []
    check_feasible(tasks, 10.0) # check empty tasks feasibility
    assert sum(t.effort_h for t in tasks) == 0.0 # total effort is zero


def test_task_invalid_importance_boundary():
    with pytest.raises(ValueError):
        Task("invalid task", 6, 2.5, date(2026, 10, 30)) # importance exceeds maximum


def test_task_days_left_past_deadline():
    task = Task("assignment", 3, 2.0, date(2026, 10, 20))
    today = date(2026, 10, 25)
    assert task.days_left(today) == 0 # deadline passed should return zero


def test_infeasible_plan_exception_attributes():
    tasks = [Task("exam", 5, 8.0, date(2026, 10, 30))]
    with pytest.raises(InfeasiblePlan) as exc_info:
        check_feasible(tasks, 5.0) # available hours insufficient
    assert exc_info.value.needed_h == 8.0 # verify needed attribute
    assert exc_info.value.available_h == 5.0 # verify available attribute