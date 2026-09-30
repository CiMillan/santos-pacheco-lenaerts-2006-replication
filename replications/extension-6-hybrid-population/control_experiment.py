"""Control experiment for the hub result: is it Q-learning, or just hubs
that never imitate? Same game, network and scale as hybrid_experiment.py.
The AI agents follow either Q-learning or one of three stubborn control
rules (control_rules.py), at a few small AI shares, random vs. hubs."""
import json
import sys
import time

sys.path.insert(0, "../..")
from main import average_trace

from control_rules import CONTROL_RULES
from hybrid_experiment import (AVG_DEGREE, GENERATIONS, M, N, NUM_REALIZATIONS, PLACEMENTS,
                               P, R, S, T, final_value)
from main_hybrid import run_batch_hybrid

RULES = ["q_learning"] + CONTROL_RULES
AI_FRACTIONS = [0.05, 0.1, 0.25]

if __name__ == "__main__":
    start = time.time()
    results = {"params": dict(R=R, S=S, T=T, P=P, N=N, realizations=NUM_REALIZATIONS, m=M,
                              alpha=0.1, tau=0.1), "runs": []}
    for rule in RULES:
        for placement in PLACEMENTS:
            for f in AI_FRACTIONS:
                traces = run_batch_hybrid("scale_free", N, GENERATIONS, R, S, T, P, NUM_REALIZATIONS,
                                          seed=1, ai_fraction=f, placement=placement, m=M,
                                          avg_degree=AVG_DEGREE, ai_rule=rule)
                row = {"rule": rule, "placement": placement, "ai_fraction": f,
                       "all": final_value(traces, "all"), "humans": final_value(traces, "humans")}
                results["runs"].append(row)
                print(f"{rule:16s} {placement:6s} AI {f:4.0%}: all={row['all']:.3f} humans={row['humans']:.3f}")
    with open("control_results.json", "w") as fh:
        json.dump(results, fh)
    print(f"saved control_results.json ({time.time() - start:.0f}s elapsed)")
