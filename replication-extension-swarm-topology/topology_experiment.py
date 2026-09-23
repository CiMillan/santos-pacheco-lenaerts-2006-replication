"""The runnable experiment: swarm fixed as the update rule, network varied
across the paper's four types, imitation re-run alongside as the baseline.
Same reduced scale as ../reduced_scale_figures.py -- see ARCHITECTURE.txt."""
import json
import sys
import time

sys.path.insert(0, "..")
from sweep import sweep

from sweep_swarm import sweep_swarm
from plot_topology import plot_topology_grid

T_values = [0.0, 0.5, 1.0, 1.5, 2.0]
S_values = [-1.0, -0.5, 0.0, 0.5, 1.0]
NETWORKS = {"complete": 200, "single_scale": 500, "scale_free_random": 500, "scale_free": 500}
NUM_REALIZATIONS = 10
TRANSIENT = 300
AVG_WINDOW = 60
GENERATIONS = TRANSIENT + AVG_WINDOW


def summarize(results):
    """
    results: {(T, S): cooperation_fraction}.
    Returns (whole-grid mean, Prisoner's Dilemma corner mean), where the PD
    corner is every grid point with T > 1 and S < 0.
    """
    pd = [c for (T, S), c in results.items() if T > 1 and S < 0]
    return sum(results.values()) / len(results), sum(pd) / len(pd)


if __name__ == "__main__":
    start = time.time()
    settings = dict(generations=GENERATIONS, T_values=T_values, S_values=S_values, R=1, P=0,
                    num_realizations=NUM_REALIZATIONS, seed=1, tail=AVG_WINDOW, m=2, avg_degree=4)

    rows = {}
    for kind, n in NETWORKS.items():
        print(f"{kind} (n={n}) -- imitation...", flush=True)
        imitation = sweep(kind, n=n, **settings)
        print(f"{kind} (n={n}) -- swarm... ({time.time() - start:.0f}s elapsed)", flush=True)
        swarm = sweep_swarm(kind, n=n, **settings)
        rows[kind] = (imitation, swarm)

    print(f"\n{'network':<18} {'imit grid':>9} {'swarm grid':>10} {'imit PD':>8} {'swarm PD':>9}")
    for kind, (imitation, swarm) in rows.items():
        ig, ipd = summarize(imitation)
        sg, spd = summarize(swarm)
        print(f"{kind:<18} {ig:9.3f} {sg:10.3f} {ipd:8.3f} {spd:9.3f}")

    with open("topology_results.json", "w") as f:
        json.dump({kind: {"imitation": {f"{T},{S}": c for (T, S), c in imi.items()},
                          "swarm": {f"{T},{S}": c for (T, S), c in swa.items()}}
                   for kind, (imi, swa) in rows.items()}, f, indent=1)

    fig = plot_topology_grid(rows, T_values, S_values,
                             suptitle="Topology effect: imitation vs. swarm, reduced scale -- cf. Fig. 2/3")
    fig.savefig("topology_swarm_vs_imitation.png", dpi=150)
    print(f"\nsaved topology_results.json + topology_swarm_vs_imitation.png ({time.time() - start:.0f}s total)")
