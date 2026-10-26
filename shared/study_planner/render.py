"""Schedule rendering and formatting."""

from .models import Task


def render(selected: list[Task], hours: float) -> str:
    """Format selected tasks into a printable schedule table.

    Args:
        selected: Tasks allocated for tonight.
        hours: Total available hours tonight.

    Returns:
        Formatted multi-line schedule string.
    """
    lines = [f"Tonight ({hours:.1f} h):"]
    if not selected:
        lines.append("No tasks fit the available time.")
        return "\n".join(lines)

    max_len = max((len(t.title) for t in selected), default=10)
    target_width = max(max_len + 6, 16)

    for index, task in enumerate(selected, start=1):
        dots_count = max(1, target_width - len(task.title))
        dots = "." * dots_count
        lines.append(f"{index:>2}. {task.title} {dots} {task.effort_h:.1f} h")

    return "\n".join(lines)

