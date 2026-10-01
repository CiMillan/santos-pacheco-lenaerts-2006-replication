"""Side by side: extension 6 on the toy network (Barabasi-Albert) vs. the
same experiment on the real FM network. Left: cooperation against AI share.
Right: 10% of the hubs, by AI rule."""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TOY = "../extension-6-hybrid-population/"
RANDOM, HUBS = "#1f3a5f", "#e4572e"
RULES = [("always_cooperate", "always C"), ("q_learning", "Q-learning"),
         ("coin_flip", "coin flip"), ("always_defect", "always D")]


def plot_fm(fm, toy_hybrid, toy_control, out="figures/fm_vs_toy.png"):
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 4.6), gridspec_kw={"width_ratios": [1.3, 1]})

    for placement, color in [("random", RANDOM), ("hubs", HUBS)]:
        toy = sorted((r["ai_fraction"], r["all"]) for r in toy_hybrid["runs"] if r["placement"] == placement)
        real = sorted((r["ai_fraction"], r["all"]) for r in fm["runs"]
                      if r["network"] == "fm" and r["rule"] == "q_learning" and r["placement"] == placement)
        left.plot(*zip(*toy), "--o", color=color, alpha=0.45, mfc="white", label=f"toy network, AI {placement}")
        left.plot(*zip(*real), "-o", color=color, label=f"FM network, AI {placement}")
    models = next(r for r in fm["runs"] if r["placement"] == "models")
    left.plot(models["ai_fraction"], models["all"], "*", ms=16, color="black",
              label="FM network, AI = every model asset")
    left.set_xlabel("share of AI agents")
    left.set_ylabel("fraction of cooperators")
    left.set_ylim(0, 1)
    left.set_title("Cooperation vs. AI share")
    left.legend(fontsize=8, frameon=False)

    toy10 = {r["rule"]: r["all"] for r in toy_control["runs"] if r["placement"] == "hubs" and r["ai_fraction"] == 0.1}
    fm10 = {r["rule"]: r["all"] for r in fm["runs"]
            if r["network"] == "fm" and r["placement"] == "hubs" and r["ai_fraction"] == 0.1}
    x = range(len(RULES))
    right.bar([i - 0.2 for i in x], [toy10[k] for k, _ in RULES], 0.4, color="#9aa5b1", label="toy network")
    right.bar([i + 0.2 for i in x], [fm10[k] for k, _ in RULES], 0.4, color=HUBS, label="FM network")
    for i, (k, _) in enumerate(RULES):
        right.text(i - 0.2, toy10[k] + 0.02, f"{toy10[k]:.2f}", ha="center", fontsize=8)
        right.text(i + 0.2, fm10[k] + 0.02, f"{fm10[k]:.2f}", ha="center", fontsize=8)
    right.set_xticks(list(x), [label for _, label in RULES])
    right.set_ylim(0, 1.08)
    right.set_title("10% AI on the hubs, by AI rule")
    right.legend(fontsize=8, frameon=False)

    fig.tight_layout()
    fig.savefig(out, dpi=150)
    print("saved", out)


if __name__ == "__main__":
    load = lambda p: json.load(open(p))
    plot_fm(load("fm_results.json"), load(TOY + "hybrid_results.json"), load(TOY + "control_results.json"))
