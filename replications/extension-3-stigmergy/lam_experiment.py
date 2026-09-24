"""The runnable experiment: stigmergic imitation on all four networks for ONE
lam value (given on the command line), with the "average" trace or the
"peak" control (optional second argument, default average). Same reduced scale, grid and seeds as
../extension-2-swarm-topology/topology_experiment.py, so results
compare directly with its saved imitation baseline (topology_results.json),
which is not rerun. Run once per lam -- separate processes run in parallel."""
import json
import sys
import time

sys.path.insert(0, "../extension-2-swarm-topology")
from sweep_stigmergy import sweep_stigmergy
from topology_experiment import T_values, S_values, NETWORKS, NUM_REALIZATIONS, GENERATIONS, AVG_WINDOW


def run_lam(lam, trace_rule="average"):
    """Stigmergy (T, S) sweep on every network at this lam.
    Returns {network_kind: {(T, S): cooperation_fraction}}."""
    return {
        kind: sweep_stigmergy(kind, n=n, generations=GENERATIONS, T_values=T_values, S_values=S_values,
                              R=1, P=0, num_realizations=NUM_REALIZATIONS, seed=1, lam=lam,
                              tail=AVG_WINDOW, m=2, avg_degree=4, trace_rule=trace_rule)
        for kind, n in NETWORKS.items()
    }


if __name__ == "__main__":
    lam = float(sys.argv[1])
    trace_rule = sys.argv[2] if len(sys.argv) > 2 else "average"
    prefix = "lam" if trace_rule == "average" else f"{trace_rule}_lam"
    start = time.time()
    results = run_lam(lam, trace_rule)
    with open(f"{prefix}_{lam}_results.json", "w") as f:
        json.dump({kind: {f"{T},{S}": c for (T, S), c in res.items()} for kind, res in results.items()}, f, indent=1)
    print(f"saved {prefix}_{lam}_results.json ({time.time() - start:.0f}s)")
