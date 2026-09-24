"""Follow-up test from CONCLUSIONS.txt: switch off swarm's personal-best
memory (c1=0) and check whether the paper's topology ordering comes back.
Everything else is identical to topology_experiment.py. Imitation is NOT
rerun -- its numbers are loaded from topology_results.json (same seeds)."""
import json
import time

from sweep_swarm import sweep_swarm
from plot_topology import plot_topology_grid
from topology_experiment import (T_values, S_values, NETWORKS, NUM_REALIZATIONS,
                                 GENERATIONS, AVG_WINDOW, summarize)


def load_results(saved):
    """Turns topology_results.json's "T,S" string keys back into (T, S) tuples."""
    return {tuple(float(x) for x in key.split(",")): c for key, c in saved.items()}


if __name__ == "__main__":
    start = time.time()
    with open("topology_results.json") as f:
        saved = json.load(f)
    settings = dict(generations=GENERATIONS, T_values=T_values, S_values=S_values, R=1, P=0,
                    num_realizations=NUM_REALIZATIONS, seed=1, tail=AVG_WINDOW, m=2, avg_degree=4)

    rows = {}
    for kind, n in NETWORKS.items():
        print(f"{kind} (n={n}) -- swarm c1=0... ({time.time() - start:.0f}s elapsed)", flush=True)
        rows[kind] = (load_results(saved[kind]["imitation"]), sweep_swarm(kind, n=n, c1=0.0, **settings))

    print(f"\n{'network':<18} {'imit grid':>9} {'c1=0 grid':>10} {'c1=1.5 grid':>12}")
    for kind, (imitation, swarm_c1_0) in rows.items():
        swarm_default, _ = summarize(load_results(saved[kind]["swarm"]))
        print(f"{kind:<18} {summarize(imitation)[0]:9.3f} {summarize(swarm_c1_0)[0]:10.3f} {swarm_default:12.3f}")

    with open("c1_zero_results.json", "w") as f:
        json.dump({kind: {f"{T},{S}": c for (T, S), c in swa.items()} for kind, (_, swa) in rows.items()}, f, indent=1)

    fig = plot_topology_grid(rows, T_values, S_values,
                             suptitle="Swarm with NO personal memory (c1=0) vs. imitation, reduced scale")
    fig.savefig("figures/topology_c1_zero.png", dpi=150)
    print(f"\nsaved c1_zero_results.json + figures/topology_c1_zero.png ({time.time() - start:.0f}s total)")
