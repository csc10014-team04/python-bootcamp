"""Week 2 Task 3: InfeasiblePlan exception and feasibility checking."""

from .models import Task


class InfeasiblePlan(Exception):
    """Raised when required study effort exceeds available hours."""

    def __init__(self, needed_h: float, available_h: float) -> None:
        """Initialize the InfeasiblePlan exception.

        Args:
            needed_h: Total hours required to complete tasks.
            available_h: Total available hours.
        """
        self.needed_h = needed_h
        self.available_h = available_h
        super().__init__(str(self))

    def __str__(self) -> str:
        """Return a readable error message describing the deficit."""
        return (
            f"Infeasible Plan: requires {self.needed_h}h, "
            f"but only {self.available_h}h available."
        )


def check_feasible(tasks: list[Task], available_h: float) -> None:
    """Check whether a list of tasks can be completed within available hours.

    Args:
        tasks: List of tasks to evaluate.
        available_h: Total available study hours.

    Raises:
        InfeasiblePlan: If total effort exceeds available hours.
    """
    needed_h = sum(t.effort_h for t in tasks)
    if needed_h > available_h:
        raise InfeasiblePlan(needed_h, available_h)
