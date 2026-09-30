"""The runnable experiment: how much cooperation survives as a growing share
of the population are AI agents (Q-learning) instead of humans (imitation)?
Same fixed Prisoner's Dilemma, same scale_free network, same reduced-scale
settings as ../extension-1-swarm-learning/compare_imitation_vs_swarm.py.
AI agents placed either at random or on the hubs -- see ARCHITECTURE.txt."""
import json
import sys
import time

sys.path.insert(0, "../..")
from main import average_trace

from main_hybrid import run_batch_hybrid

R, S, T, P = 1, -0.1, 1.2, 0
N = 500
NUM_REALIZATIONS = 10
TRANSIENT = 300
AVG_WINDOW = 60
GENERATIONS = TRANSIENT + AVG_WINDOW
M, AVG_DEGREE = 2, 4
AI_FRACTIONS = [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]
PLACEMENTS = ["random", "hubs"]
GROUPS = ["all", "humans", "ai", "hubs"]


def final_value(traces, group):
    """Mean over the last AVG_WINDOW generations of the realization-averaged
    trace for one group; None if the group is empty (e.g. no AI at 0%)."""
    group_traces = [t[group] for t in traces]
    if group_traces[0][0] is None:
        return None
    avg = average_trace(group_traces)
    return sum(avg[-AVG_WINDOW:]) / AVG_WINDOW


if __name__ == "__main__":
    start = time.time()
    results = {"params": dict(R=R, S=S, T=T, P=P, N=N, realizations=NUM_REALIZATIONS,
                              transient=TRANSIENT, window=AVG_WINDOW, m=M, alpha=0.1, tau=0.1),
               "runs": []}
    for placement in PLACEMENTS:
        for f in AI_FRACTIONS:
            traces = run_batch_hybrid("scale_free", N, GENERATIONS, R, S, T, P, NUM_REALIZATIONS,
                                      seed=1, ai_fraction=f, placement=placement, m=M, avg_degree=AVG_DEGREE)
            row = {"placement": placement, "ai_fraction": f}
            row.update({g: final_value(traces, g) for g in GROUPS})
            row["trace_all"] = average_trace([t["all"] for t in traces])
            results["runs"].append(row)
            show = " ".join(f"{g}={row[g]:.3f}" if row[g] is not None else f"{g}=--" for g in GROUPS)
            print(f"{placement:6s} AI {f:4.0%}: {show}")
    with open("hybrid_results.json", "w") as fh:
        json.dump(results, fh)
    print(f"saved hybrid_results.json ({time.time() - start:.0f}s elapsed)")
