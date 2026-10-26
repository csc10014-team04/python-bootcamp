"""Chat log and API route latency statistics analyzer."""

import math
from collections import Counter, defaultdict
from collections.abc import Sequence
from typing import Any


def analyse(
    pairs: Sequence[tuple[str, float]] | list[tuple[str, float]],
) -> dict[str, Any]:
    """Analyze a list of (route, latency_ms) pairs.

    Computes:
        - counts: Number of requests per route (Counter).
        - p95: The 95th percentile latency per route.
        - slowest: The route name with the highest p95 latency.

    Args:
        pairs: Sequence of (route, latency_ms) tuples.

    Returns:
        A dictionary containing "counts", "p95", and "slowest".
    """
    counts: Counter[str] = Counter()
    latencies: defaultdict[str, list[float]] = defaultdict(list)

    for route, latency_ms in pairs:
        counts[route] += 1
        latencies[route].append(latency_ms)

    p95: dict[str, float] = {}
    for route, values in latencies.items():
        values.sort()
        index = math.ceil(0.95 * len(values)) - 1
        p95[route] = values[index]

    slowest: str | None = max(p95, key=p95.get) if p95 else None

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }
