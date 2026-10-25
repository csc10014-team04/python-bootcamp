from collections import Counter,defaultdict
import math

def analyse(pairs):
    counts=Counter()
    latencies=defaultdict(list)

    for route,latency_ms in pairs:
        counts[route]+=1
        latencies[route].append(latency_ms)

    p95={}
    for route,values in latencies.items():
        values.sort()
        index=math.ceil(0.95*len(values))-1
        p95[route]=values[index]

    slowest=max(p95,key=p95.get) if p95 else None

    return {
        "counts":counts,
        "p95":p95,
        "slowest":slowest
    }