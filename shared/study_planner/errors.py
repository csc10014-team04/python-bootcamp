"""Custom exception classes for the study planner."""


class StudyPlannerError(Exception):
    """Base exception for all study planner errors."""


class EmptyFileError(StudyPlannerError):
    """Raised when the CSV task file is empty or contains no tasks."""


class InfeasiblePlan(StudyPlannerError):
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

