"""Is the all-human peak in beta_sweep.py real, or noise from 10 runs?
Same sweep, all human, beta 0.1 to 10 only, 50 realizations instead of 10.
Also prints the share of runs that end with every node cooperating, since
single runs tend to end all-C or all-D and the mean hides that."""
import json
import sys
import time

sys.path.insert(0, "../extension-6-hybrid-population")
from hybrid_experiment import AVG_DEGREE, GENERATIONS, M, N, P, R, S, T, final_value

from beta_sweep import BETAS
from main_fermi import run_batch_fermi

NUM_REALIZATIONS = 50
PEAK_BETAS = [b for b in BETAS if b >= 0.1]

if __name__ == "__main__":
    start = time.time()
    results = {"params": dict(R=R, S=S, T=T, P=P, N=N, realizations=NUM_REALIZATIONS, m=M,
                              generations=GENERATIONS, ai_fraction=0.0), "runs": []}
    for beta in PEAK_BETAS:
        traces = run_batch_fermi("scale_free", N, GENERATIONS, R, S, T, P, NUM_REALIZATIONS,
                                 seed=1, beta=beta, m=M, avg_degree=AVG_DEGREE)
        all_c = sum(t["all"][-1] == 1.0 for t in traces) / NUM_REALIZATIONS
        row = {"beta": beta, "all": final_value(traces, "all"), "runs_all_c": all_c}
        results["runs"].append(row)
        print(f"beta {beta:7.4f}: all={row['all']:.3f} runs ending all-C={all_c:.2f}")
    with open("peak_results.json", "w") as fh:
        json.dump(results, fh)
    print(f"saved peak_results.json ({time.time() - start:.0f}s elapsed)")
