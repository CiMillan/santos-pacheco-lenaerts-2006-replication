"""The runnable experiment: which selection pressure beta maximizes cooperation
in our simulation? Pinheiro, Santos & Pacheco (2012) find an intermediate beta
that does, on BA networks. Sweep beta over their range (0.01 to 10), all human,
then again with 10% AI agents on the hubs. Same game, network and scale as
../extension-6-hybrid-population/hybrid_experiment.py."""
import json
import sys
import time

sys.path.insert(0, "../extension-6-hybrid-population")
from hybrid_experiment import AVG_DEGREE, GENERATIONS, M, N, NUM_REALIZATIONS, P, R, S, T, final_value

from main_fermi import run_batch_fermi

BETAS = [round(10 ** (k / 4), 4) for k in range(-8, 5)]  # 0.01 ... 10, four per decade
AI_FRACTIONS = [0.0, 0.1]

if __name__ == "__main__":
    start = time.time()
    results = {"params": dict(R=R, S=S, T=T, P=P, N=N, realizations=NUM_REALIZATIONS, m=M,
                              generations=GENERATIONS, placement="hubs", alpha=0.1, tau=0.1),
               "runs": []}
    for f in AI_FRACTIONS:
        for beta in BETAS:
            traces = run_batch_fermi("scale_free", N, GENERATIONS, R, S, T, P, NUM_REALIZATIONS,
                                     seed=1, beta=beta, ai_fraction=f, m=M, avg_degree=AVG_DEGREE)
            row = {"ai_fraction": f, "beta": beta, "all": final_value(traces, "all"),
                   "hubs": final_value(traces, "hubs")}
            results["runs"].append(row)
            print(f"AI {f:4.0%} beta {beta:7.4f}: all={row['all']:.3f} hubs={row['hubs']:.3f}")
    with open("beta_results.json", "w") as fh:
        json.dump(results, fh)
    print(f"saved beta_results.json ({time.time() - start:.0f}s elapsed)")
