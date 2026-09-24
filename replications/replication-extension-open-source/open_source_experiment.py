"""The runnable experiment: imitation over PROGRAMS on all four networks,
compared against plain C/D imitation. Same reduced scale and seeds as
../replication-extension-swarm-topology/topology_experiment.py; plain
imitation is NOT rerun, its numbers come from that folder's
topology_results.json. See ARCHITECTURE.txt."""
import json
import sys
import time

sys.path.insert(0, "../replication-extension-swarm-topology")
from topology_experiment import T_values, S_values, NETWORKS, NUM_REALIZATIONS, GENERATIONS, AVG_WINDOW, summarize
from c1_zero_experiment import load_results
from plot_topology import plot_topology_grid

from programs import PROGRAMS
from sweep_os import sweep_os


def mean_shares(shares, pd_only=False):
    """
    shares: {(T, S): {program: share}} from sweep_os().
    Returns {program: mean share} over the whole grid, or only over the
    Prisoner's Dilemma corner (T > 1, S < 0) if pd_only.
    """
    points = [pt for pt in shares if not pd_only or (pt[0] > 1 and pt[1] < 0)]
    return {p: sum(shares[pt][p] for pt in points) / len(points) for p in PROGRAMS}


if __name__ == "__main__":
    start = time.time()
    with open("../replication-extension-swarm-topology/topology_results.json") as f:
        saved = json.load(f)
    settings = dict(generations=GENERATIONS, T_values=T_values, S_values=S_values, R=1, P=0,
                    num_realizations=NUM_REALIZATIONS, seed=1, tail=AVG_WINDOW, m=2, avg_degree=4)

    rows, all_shares = {}, {}
    for kind, n in NETWORKS.items():
        print(f"{kind} (n={n}) -- open-source imitation... ({time.time() - start:.0f}s elapsed)", flush=True)
        cooperation, shares = sweep_os(kind, n=n, **settings)
        rows[kind] = (load_results(saved[kind]["imitation"]), cooperation)
        all_shares[kind] = shares

    print(f"\n{'network':<18} {'plain grid':>10} {'open grid':>9} {'plain PD':>9} {'open PD':>8}")
    for kind, (plain, open_source) in rows.items():
        pg, ppd = summarize(plain)
        og, opd = summarize(open_source)
        print(f"{kind:<18} {pg:10.3f} {og:9.3f} {ppd:9.3f} {opd:8.3f}")

    for label, pd_only in [("whole grid", False), ("PD corner", True)]:
        print(f"\nfinal program shares, {label}:")
        print(f"{'network':<18} " + " ".join(f"{p:>12}" for p in PROGRAMS))
        for kind in rows:
            ms = mean_shares(all_shares[kind], pd_only)
            print(f"{kind:<18} " + " ".join(f"{ms[p]:12.3f}" for p in PROGRAMS))

    with open("open_source_results.json", "w") as f:
        json.dump({kind: {"cooperation": {f"{T},{S}": c for (T, S), c in rows[kind][1].items()},
                          "shares": {f"{T},{S}": s for (T, S), s in all_shares[kind].items()}}
                   for kind in rows}, f, indent=1)

    fig = plot_topology_grid(rows, T_values, S_values, labels=("plain imitation", "open-source"),
                             suptitle="Open-source programs vs. plain C/D imitation, reduced scale -- cf. Fig. 2/3")
    fig.savefig("figures/open_source_vs_imitation.png", dpi=150)
    print(f"\nsaved open_source_results.json + figures/open_source_vs_imitation.png ({time.time() - start:.0f}s total)")
