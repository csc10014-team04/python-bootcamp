from collections.abc import Iterable
from .models import Task


class InfeasiblePlan(Exception):
    """Raised when total hours required exceed the available hours"""

    def __init__(self, needed_h: float, available_h: float):
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(
            f"Plan is infeasible: requires {needed_h:.1f}h, but only {available_h:.1f}h available "
            f"(deficit of {needed_h - available_h:.1f}h)."
        )


def check_feasible(tasks: Iterable[Task], available_h: float) -> float:
    """Checks if the total effort required by Task objects fits within available_h and raises InfeasiblePlan if needed_h > available_h; else return needed_h"""
    needed_h = sum(task.effort_h for task in tasks)

    if needed_h > available_h:
        raise InfeasiblePlan(needed_h=needed_h, available_h=available_h)

    return needed_h