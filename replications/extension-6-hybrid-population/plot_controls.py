"""Plots control_results.json and tau_results.json (made by
control_experiment.py and tau_sweep.py). Doesn't run any simulation.
Left: final cooperation at 10% AI, for Q-learning and the three stubborn
control rules, random vs. hubs. Right: final cooperation vs. tau at 10% AI."""
import json

import matplotlib.pyplot as plt

COLOURS = {"random": "#17a398", "hubs": "#e4572e"}
LABELS = {"random": "AI placed at random", "hubs": "AI placed on the hubs"}
RULE_NAMES = {"q_learning": "Q-learning", "always_defect": "always D",
              "always_cooperate": "always C", "coin_flip": "coin flip"}
BASELINE = 0.899  # 0% AI, from hybrid_experiment.py


def plot_controls(controls, taus, fraction=0.1):
    """controls, taus: the dicts saved by control_experiment.py and tau_sweep.py.
    Returns the Figure."""
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 4.5))

    rules = list(RULE_NAMES)
    width = 0.38
    for i, placement in enumerate(["random", "hubs"]):
        values = [next(r["all"] for r in controls["runs"] if r["rule"] == rule and
                       r["placement"] == placement and r["ai_fraction"] == fraction) for rule in rules]
        xs = [j + (i - 0.5) * width for j in range(len(rules))]
        left.bar(xs, values, width, color=COLOURS[placement], label=LABELS[placement])
    left.axhline(BASELINE, color="#1f3a5f", linestyle="--", label="no AI (0.90)")
    left.set_xticks(range(len(rules)), [RULE_NAMES[r] for r in rules])
    left.set_ylabel("fraction of cooperators")
    left.set_ylim(0, 1.05)
    left.set_title(f"{fraction:.0%} AI agents: learning vs. stubborn")
    left.legend(loc="upper left", fontsize=9)

    for placement in ["random", "hubs"]:
        rows = [r for r in taus["runs"] if r["placement"] == placement]
        right.plot([r["tau"] for r in rows], [r["all"] for r in rows], "o-",
                   color=COLOURS[placement], label=LABELS[placement])
    right.axhline(BASELINE, color="#1f3a5f", linestyle="--", label="no AI (0.90)")
    right.axvline(0.1, color="#5b6577", linestyle=":", label="tau used (0.1)")
    right.set_xscale("log")
    right.set_xlabel("AI exploration temperature tau (log scale)")
    right.set_ylabel("fraction of cooperators")
    right.set_ylim(0, 1.05)
    right.set_title(f"{fraction:.0%} Q-learning AI agents, varying tau")
    right.legend(fontsize=9)

    fig.tight_layout()
    return fig


if __name__ == "__main__":
    with open("control_results.json") as fh:
        controls = json.load(fh)
    with open("tau_results.json") as fh:
        taus = json.load(fh)
    plot_controls(controls, taus).savefig("figures/controls_and_tau.png", dpi=150)
    print("saved figures/controls_and_tau.png")
