"""Check whether a set of tasks fits within an available time budget."""

from w2.w2_1 import Task


class InfeasiblePlan(Exception):
    """Raised when the estimated task effort exceeds available time."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Store the required and available hours."""
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(self.__str__())

    def __str__(self) -> str:
        """Return a readable explanation of the infeasible plan."""
        return (
            f"Plan is infeasible: need {self.needed_h:.2f} hours, "
            f"but only {self.available_h:.2f} hours are available."
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Raise InfeasiblePlan if task effort exceeds available hours."""
    if available_h < 0:
        raise ValueError("available_h cannot be negative")
    needed_h = sum(task.effort_h for task in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
