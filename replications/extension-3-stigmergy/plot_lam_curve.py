"""Cooperation vs. lam (how fast a trace forgets), one line per network, one
panel per trace rule -- shows whether the topology effect survives
stigmergic memory. Reads the saved JSON results; runs no simulation itself."""
import json
import sys

import matplotlib.pyplot as plt

sys.path.insert(0, "../extension-2-swarm-topology")
from c1_zero_experiment import load_results
from topology_experiment import summarize

# Same validated categorical palette as ../extension-2-swarm-topology/plot_c1_curve.py.
COLORS = {"complete": "#2a78d6", "single_scale": "#eb6834",
          "scale_free_random": "#1baf7a", "scale_free": "#eda100"}
LAMS = [1.0, 0.5, 0.2, 0.05]
RULES = {"average": "lam", "peak": "peak_lam", "strategy": "strategy_lam"}


def collect_summaries():
    """Returns {rule: {network: [grid_mean at each of LAMS]}}. lam=1 is the
    paper's rule for every trace rule, read from the saved imitation
    baseline (../extension-2-swarm-topology/topology_results.json)."""
    with open("../extension-2-swarm-topology/topology_results.json") as f:
        base = json.load(f)
    summaries = {}
    for rule, prefix in RULES.items():
        summaries[rule] = {kind: [summarize(load_results(base[kind]["imitation"]))[0]] for kind in base}
        for lam in LAMS[1:]:
            with open(f"{prefix}_{lam}_results.json") as f:
                saved = json.load(f)
            for kind, res in saved.items():
                summaries[rule][kind].append(summarize(load_results(res))[0])
    return summaries


def plot_lam_curves(summaries):
    """Three panels side by side, one per trace rule: whole-grid mean vs. lam,
    lam decreasing left to right (memory gets longer). Each line is
    labelled at its right end, nudged apart so labels never overlap.
    Returns the Figure."""
    titles = {"average": "average trace\n(remembers payoff)",
              "peak": "peak trace\n(remembers best payoff)",
              "strategy": "strategy memory\n(remembers strategy behind best payoff)"}
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    xs = list(range(len(LAMS)))
    for ax, (rule, nets) in zip(axes, summaries.items()):
        for kind, ys in nets.items():
            ax.plot(xs, ys, color=COLORS[kind], linewidth=2, marker="o", markersize=6, label=kind)
        label_ys = sorted((ys[-1], kind) for kind, ys in nets.items())
        for i in range(1, len(label_ys)):  # keep a 0.018 gap from the label below
            label_ys[i] = (max(label_ys[i][0], label_ys[i - 1][0] + 0.018), label_ys[i][1])
        for y, kind in label_ys:
            ax.text(xs[-1] + 0.15, y, kind, ha="left", va="center", fontsize=8, color="#333333")
        ax.set_xticks(xs, ["1\n(paper)", "0.5", "0.2", "0.05"])
        ax.set_xlim(-0.3, len(LAMS) + 0.9)  # room on the right for labels
        ax.set_xlabel("lam (smaller = longer memory)")
        ax.set_title(titles[rule], fontsize=10)
        ax.grid(alpha=0.25)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].set_ylabel("mean fraction of cooperators, whole (T, S) grid")
    axes[0].set_ylim(0.4, 0.75)
    axes[0].legend(loc="lower left", fontsize=8, frameon=False, ncol=2)
    fig.suptitle("Stigmergic imitation: topology effect vs. memory in the environment (reduced scale)")
    fig.tight_layout()
    return fig
