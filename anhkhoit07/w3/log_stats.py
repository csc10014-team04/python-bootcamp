import math
from collections import Counter, defaultdict


def analyse(pairs: list[tuple[str, float | int]]) -> dict:
    counts = Counter() # counter for request frequencies
    latencies_by_route = defaultdict(list)

    for route, latency in pairs:
        counts[route] += 1 # tally request count
        latencies_by_route[route].append(latency)

    p95_by_route = {}
    for route, latencies in latencies_by_route.items():
        latencies.sort()
        n = len(latencies)
        rank = math.ceil(0.95 * n) # calculate nearest rank for 95th percentile
        p95_by_route[route] = latencies[max(0, rank - 1)]

    slowest_route = None
    if p95_by_route:
        slowest_route = max(p95_by_route, key=p95_by_route.get) # select route with max p95

    return {
        "counts": counts,
        "p95": p95_by_route,
        "slowest": slowest_route
    }