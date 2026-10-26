"""Task data model for the study planner."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Represents an academic study task.

    Attributes:
        title: The task name or subject.
        importance: Priority score from 1 (lowest) to 5 (highest).
        effort_h: Estimated effort in hours.
        deadline: Due date.
    """

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        """Validate task fields upon initialization.

        Raises:
            ValueError: If importance is not between 1 and 5.
        """
        if not 1 <= self.importance <= 5:
            raise ValueError("Importance must be from 1 to 5")

    def days_left(self, today: date) -> int:
        """Calculate the non-negative days remaining until the deadline.

        Args:
            today: Reference anchor date.

        Returns:
            Number of days remaining, clamped at a minimum of 0.
        """
        delta = (self.deadline - today).days
        return max(0, delta)
