"""Define the task model used by the planning exercises."""

from dataclasses import dataclass
from datetime import date


@dataclass
class Task:
    """Represent a task with an importance, effort estimate, and deadline."""

    title: str
    importance: int
    effort_h: float
    deadline: date

    def __post_init__(self) -> None:
        """Validate task fields after dataclass initialization."""
        if not 1 <= self.importance <= 5:
            raise ValueError("importance must be 1-5")
        if self.effort_h < 0:
            raise ValueError("effort_h cannot be negative")

    def days_left(self, today: date) -> int:
        """Return non-negative days remaining until the deadline."""
        return max(0, (self.deadline - today).days)
