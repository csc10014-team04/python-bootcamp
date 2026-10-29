"""Analyze request counts and p95 latency grouped by route."""

import math
from collections import Counter, defaultdict
from collections.abc import Iterable
from typing import TypedDict


class RouteAnalysis(TypedDict):
    """Describe the output produced by analyse."""

    counts: Counter[str]
    p95: dict[str, float]
    slowest: str | None


def analyse(pairs: Iterable[tuple[str, float]]) -> RouteAnalysis:
    """Return route counts, p95 latencies, and the slowest route."""
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

    slowest = max(p95, key=p95.get) if p95 else None
    return {"counts": counts, "p95": p95, "slowest": slowest}
