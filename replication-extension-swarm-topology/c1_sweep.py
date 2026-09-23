"""Intermediate c1 values: where does the topology effect disappear?
Runs swarm on all four networks for ONE c1 value (given on the command
line), with everything else identical to topology_experiment.py. Run once
per c1 value -- separate processes can run in parallel on separate cores.
c1=0 and c1=1.5 are already saved (c1_zero_results.json,
topology_results.json), so they aren't rerun."""
import json
import sys
import time

from sweep_swarm import sweep_swarm
from topology_experiment import T_values, S_values, NETWORKS, NUM_REALIZATIONS, GENERATIONS, AVG_WINDOW


def run_c1(c1):
    """Swarm (T, S) sweep on every network at this c1.
    Returns {network_kind: {(T, S): cooperation_fraction}}."""
    return {
        kind: sweep_swarm(kind, n=n, generations=GENERATIONS, T_values=T_values, S_values=S_values,
                          R=1, P=0, num_realizations=NUM_REALIZATIONS, seed=1, tail=AVG_WINDOW,
                          m=2, avg_degree=4, c1=c1)
        for kind, n in NETWORKS.items()
    }


if __name__ == "__main__":
    c1 = float(sys.argv[1])
    start = time.time()
    results = run_c1(c1)
    with open(f"c1_{c1}_results.json", "w") as f:
        json.dump({kind: {f"{T},{S}": c for (T, S), c in res.items()} for kind, res in results.items()}, f, indent=1)
    print(f"saved c1_{c1}_results.json ({time.time() - start:.0f}s)")
