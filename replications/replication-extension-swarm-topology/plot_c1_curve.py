"""Cooperation vs. c1 (swarm's personal-memory weight), one line per network
-- shows where the topology effect disappears as memory gets stronger.
Reads the saved JSON results; runs no simulation itself."""
import json
import os

import matplotlib.pyplot as plt

from c1_zero_experiment import load_results
from topology_experiment import summarize

# Validated categorical palette (dataviz skill), fixed order, one per network.
COLORS = {"complete": "#2a78d6", "single_scale": "#eb6834",
          "scale_free_random": "#1baf7a", "scale_free": "#eda100"}


def collect_summaries():
    """Returns {network: [(c1, grid_mean, pd_mean), ...]} sorted by c1, from
    every results file that exists: c1=0 (c1_zero_results.json), c1=1.5
    (the "swarm" part of topology_results.json), and c1_<value>_results.json."""
    files = {0.0: "c1_zero_results.json", 1.5: "topology_results.json"}
    for c1 in [0.25, 0.5, 1.0]:
        files[c1] = f"c1_{c1}_results.json"

    summaries = {}
    for c1, path in sorted(files.items()):
        if not os.path.exists(path):
            continue
        with open(path) as f:
            saved = json.load(f)
        for kind, res in saved.items():
            res = res["swarm"] if c1 == 1.5 else res
            summaries.setdefault(kind, []).append((c1, *summarize(load_results(res))))
    return summaries


def plot_c1_curves(summaries):
    """Two panels side by side: whole-grid mean and PD-corner mean vs. c1.
    Each line is labelled at its LEFT end (c1=0, where the networks are
    most spread out), nudged apart so labels never overlap, so identity
    never relies on colour alone. Returns the Figure."""
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for ax, col, title in [(axes[0], 1, "whole (T, S) grid"), (axes[1], 2, "Prisoner's Dilemma corner (T>1, S<0)")]:
        for kind, points in summaries.items():
            xs = [p[0] for p in points]
            ys = [p[col] for p in points]
            ax.plot(xs, ys, color=COLORS[kind], linewidth=2, marker="o", markersize=6, label=kind)

        label_ys = sorted((points[0][col], kind) for kind, points in summaries.items())
        for i in range(1, len(label_ys)):  # push each label up to keep a 0.045 gap from the one below
            label_ys[i] = (max(label_ys[i][0], label_ys[i - 1][0] + 0.045), label_ys[i][1])
        for y, kind in label_ys:
            ax.text(-0.08, y, kind, ha="right", va="center", fontsize=8, color="#333333")
        ax.set_xlabel("c1 (weight of personal-best memory)")
        ax.set_ylabel("mean fraction of cooperators")
        ax.set_ylim(0, 1)
        ax.set_xlim(-0.75, 1.6)  # room on the left for labels
        ax.set_xticks([0, 0.25, 0.5, 1.0, 1.5])
        ax.set_title(title)
        ax.grid(alpha=0.25)
        ax.spines[["top", "right"]].set_visible(False)
    axes[0].legend(loc="lower left", fontsize=8, frameon=False)
    fig.suptitle("Swarm: topology effect vs. strength of personal memory (reduced scale)")
    fig.tight_layout()
    return fig
