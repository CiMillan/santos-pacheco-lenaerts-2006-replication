"""Robustness check: does the result depend on the AI agents' exploration
temperature tau? tau = 0.1 was a design choice with no source, so sweep it,
at 10% Q-learning AI agents, random vs. hubs. Same game, network and scale
as hybrid_experiment.py; alpha stays 0.1."""
import json
import sys
import time

sys.path.insert(0, "../..")

from hybrid_experiment import (AVG_DEGREE, GENERATIONS, M, N, NUM_REALIZATIONS, PLACEMENTS,
                               P, R, S, T, final_value)
from main_hybrid import run_batch_hybrid

TAUS = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0]
AI_FRACTION = 0.1

if __name__ == "__main__":
    start = time.time()
    results = {"params": dict(R=R, S=S, T=T, P=P, N=N, realizations=NUM_REALIZATIONS, m=M,
                              alpha=0.1, ai_fraction=AI_FRACTION), "runs": []}
    for placement in PLACEMENTS:
        for tau in TAUS:
            traces = run_batch_hybrid("scale_free", N, GENERATIONS, R, S, T, P, NUM_REALIZATIONS,
                                      seed=1, ai_fraction=AI_FRACTION, placement=placement,
                                      tau=tau, m=M, avg_degree=AVG_DEGREE)
            row = {"placement": placement, "tau": tau,
                   "all": final_value(traces, "all"), "ai": final_value(traces, "ai")}
            results["runs"].append(row)
            print(f"{placement:6s} tau {tau:5.2f}: all={row['all']:.3f} ai={row['ai']:.3f}")
    with open("tau_results.json", "w") as fh:
        json.dump(results, fh)
    print(f"saved tau_results.json ({time.time() - start:.0f}s elapsed)")
