"""Alias for W2 package to support lowercase module imports."""

try:
    from . import W2
except ImportError:
    import W2

__all__ = W2.__all__
Task = W2.Task
load_tasks = W2.load_tasks
save_json = W2.save_json
InfeasiblePlan = W2.InfeasiblePlan
check_feasible = W2.check_feasible
