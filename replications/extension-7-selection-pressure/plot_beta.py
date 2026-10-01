"""Plots beta_results.json and peak_results.json (made by beta_sweep.py and
peak_check.py). Doesn't run any simulation. Final cooperation vs. the human
selection pressure beta: all human (10 and 50 runs) and with 10% AI hubs."""
import json

import matplotlib.pyplot as plt

HUMAN, AI = "#1f3a5f", "#e4572e"
BASELINE = 0.899  # all human, Santos rule, from ../extension-6-hybrid-population


def plot_beta(sweep, peak):
    """sweep, peak: the dicts saved by beta_sweep.py and peak_check.py. Returns the Figure."""
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    for f, colour, label in [(0.0, HUMAN, "all human (10 runs)"), (0.1, AI, "10% AI on the hubs (10 runs)")]:
        rows = [r for r in sweep["runs"] if r["ai_fraction"] == f]
        ax.plot([r["beta"] for r in rows], [r["all"] for r in rows], "o-", color=colour, label=label)
    ax.plot([r["beta"] for r in peak["runs"]], [r["all"] for r in peak["runs"]], "s--", color=HUMAN,
            mfc="white", label="all human (50 runs)")
    best = max(peak["runs"], key=lambda r: r["all"])
    ax.annotate(f"best beta = {best['beta']:.2f}", (best["beta"], best["all"]), xytext=(0.02, 0.97),
                arrowprops=dict(arrowstyle="->", color="#5b6577"), fontsize=9)
    ax.axhline(BASELINE, color="#5b6577", linestyle=":", label="all human, Santos rule (0.90)")
    ax.set_xscale("log")
    ax.set_xlabel("human selection pressure beta (log scale)")
    ax.set_ylabel("fraction of cooperators")
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=9, loc="center right")
    fig.tight_layout()
    return fig


if __name__ == "__main__":
    with open("beta_results.json") as fh:
        sweep = json.load(fh)
    with open("peak_results.json") as fh:
        peak = json.load(fh)
    plot_beta(sweep, peak).savefig("figures/beta_sweep.png", dpi=150)
    print("saved figures/beta_sweep.png")
