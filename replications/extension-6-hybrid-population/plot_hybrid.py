"""Plots hybrid_results.json (made by hybrid_experiment.py). Doesn't run
any simulation, just visualizes saved results.
Left: final cooperation vs. share of AI agents, random vs. hub placement.
Right: cooperation over time at 10% AI, against the all-human baseline."""
import json

import matplotlib.pyplot as plt

COLOURS = {"random": "#17a398", "hubs": "#e4572e"}
LABELS = {"random": "AI placed at random", "hubs": "AI placed on the hubs"}


def plot_hybrid(results, highlight_fraction=0.1):
    """results: the dict saved by hybrid_experiment.py. Returns the Figure."""
    runs = results["runs"]
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 4.5))

    for placement in ["random", "hubs"]:
        rows = [r for r in runs if r["placement"] == placement]
        left.plot([100 * r["ai_fraction"] for r in rows], [r["all"] for r in rows],
                  "o-", color=COLOURS[placement], label=LABELS[placement])
    left.set_xlabel("share of AI agents (%)")
    left.set_ylabel("fraction of cooperators")
    left.set_ylim(0, 1)
    left.set_title("Final cooperation (last 60 generations)")
    left.legend()

    baseline = next(r for r in runs if r["ai_fraction"] == 0.0)
    right.plot(baseline["trace_all"], color="#1f3a5f", label="all humans (paper's rule)")
    for placement in ["random", "hubs"]:
        row = next(r for r in runs if r["placement"] == placement and r["ai_fraction"] == highlight_fraction)
        right.plot(row["trace_all"], color=COLOURS[placement], label=f"{highlight_fraction:.0%} AI, {LABELS[placement][10:]}")
    right.set_xlabel("generation")
    right.set_ylabel("fraction of cooperators")
    right.set_ylim(0, 1)
    right.set_title(f"Over time, {highlight_fraction:.0%} AI agents")
    right.legend()

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    with open("hybrid_results.json") as fh:
        results = json.load(fh)
    plot_hybrid(results).savefig("figures/hybrid_population.png", dpi=150)
    print("saved figures/hybrid_population.png")
