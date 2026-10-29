from collections import Counter, defaultdict
import math


def analyse(pairs: list[tuple[str, float | int]]) -> dict:
    if not pairs:
        return {"counts": Counter(), "p95": {}, "slowest": None}

    latencies_by_route = defaultdict(list)
    counts = Counter()

    for route, latency in pairs:
        latencies_by_route[route].append(latency)
        counts[route] += 1

    p95 = {}
    for route, values in latencies_by_route.items():
        sorted_vals = sorted(values)
        n = len(sorted_vals)

        idx = max(0, math.ceil(0.95 * n) - 1)
        p95[route] = sorted_vals[idx]

    slowest = max(p95, key=p95.get)

    return {
        "counts": counts,
        "p95": p95,
        "slowest": slowest,
    }