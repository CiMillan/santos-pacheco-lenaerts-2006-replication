"""Proof-cost follow-up (Critch et al. Open Problem 9): the open-source
experiment again, but code-reading programs (CliqueBot, FairBot,
PrudentBot) pay `cost` per game. Run once per cost value, from the command
line, so several values can run in parallel -- like
../replication-extension-swarm-topology/c1_sweep.py.
  python3 cost_experiment.py 0.2
Saves cost_<value>_results.json in open_source_results.json's format."""
import json
import sys
import time

sys.path.insert(0, "../replication-extension-swarm-topology")
from topology_experiment import T_values, S_values, NETWORKS, NUM_REALIZATIONS, GENERATIONS, AVG_WINDOW, summarize

from sweep_os import sweep_os
from open_source_experiment import mean_shares


def run_cost(cost):
    """All four networks at one cost value. Returns {network: (cooperation, shares)}."""
    settings = dict(generations=GENERATIONS, T_values=T_values, S_values=S_values, R=1, P=0,
                    num_realizations=NUM_REALIZATIONS, seed=1, tail=AVG_WINDOW, m=2, avg_degree=4)
    return {kind: sweep_os(kind, n=n, cost=cost, **settings) for kind, n in NETWORKS.items()}


if __name__ == "__main__":
    cost = float(sys.argv[1])
    start = time.time()
    results = run_cost(cost)
    print(f"cost={cost}  ({time.time() - start:.0f}s)")
    print(f"{'network':<18} {'grid':>6} {'PD':>6}   PD-corner shares (Coop Defect Clique Fair Prudent)")
    for kind, (cooperation, shares) in results.items():
        g, pd = summarize(cooperation)
        ms = mean_shares(shares, pd_only=True)
        print(f"{kind:<18} {g:6.3f} {pd:6.3f}   " + " ".join(f"{v:.3f}" for v in ms.values()))

    with open(f"cost_{cost}_results.json", "w") as f:
        json.dump({kind: {"cooperation": {f"{T},{S}": c for (T, S), c in coop.items()},
                          "shares": {f"{T},{S}": s for (T, S), s in sh.items()}}
                   for kind, (coop, sh) in results.items()}, f, indent=1)
