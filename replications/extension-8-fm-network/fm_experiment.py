"""The runnable experiment: extension 6 on the real FM network. Same game,
same humans and AI agents, same scale settings as
../extension-6-hybrid-population/hybrid_experiment.py; only the network
changes. Three blocks:
  1. AI share 0-100%, at random vs. on the hubs (Q-learning AI);
  2. "models": every model asset is an AI agent (41%);
  3. controls at 10% on the hubs (stubborn AI agents), as in control_experiment.py;
  4. null model: the same degrees, links rewired at random (0% and 10% hubs)."""
import json
import sys
import time

sys.path.insert(0, "../extension-6-hybrid-population")
from control_rules import CONTROL_RULES
from hybrid_experiment import GENERATIONS, NUM_REALIZATIONS, P, R, S, T, final_value

from fm_network import load_fm_giant, rewire_keep_degrees
from main_fm import run_batch_graph

AI_FRACTIONS = [0.0, 0.1, 0.25, 0.5, 1.0]
PLACEMENTS = ["random", "hubs"]


def run_row(graph, network, ai_fraction, placement, ai_rule="q_learning"):
    traces = run_batch_graph(graph, GENERATIONS, R, S, T, P, NUM_REALIZATIONS, seed=1,
                             ai_fraction=ai_fraction, placement=placement, ai_rule=ai_rule)
    row = {"network": network, "rule": ai_rule, "placement": placement, "ai_fraction": ai_fraction,
           "all": final_value(traces, "all"), "humans": final_value(traces, "humans"),
           "ai": final_value(traces, "ai"), "hubs": final_value(traces, "hubs")}
    fmt = lambda x: "  -  " if x is None else f"{x:.3f}"
    print(f"{network:8s} {ai_rule:16s} {placement:6s} AI {ai_fraction:4.0%}: all={fmt(row['all'])} "
          f"humans={fmt(row['humans'])} ai={fmt(row['ai'])} hubs={fmt(row['hubs'])}")
    return row


if __name__ == "__main__":
    start = time.time()
    fm = load_fm_giant()
    shuffled = rewire_keep_degrees(fm, seed=1)
    rows = []
    for placement in PLACEMENTS:
        for f in AI_FRACTIONS:
            rows.append(run_row(fm, "fm", f, placement))
    models_share = sum(t == "model" for _, t in fm.nodes(data="type")) / fm.number_of_nodes()
    rows.append(run_row(fm, "fm", round(models_share, 3), "models"))
    for rule in CONTROL_RULES:
        rows.append(run_row(fm, "fm", 0.1, "hubs", rule))
    for f in [0.0, 0.1]:
        rows.append(run_row(shuffled, "rewired", f, "hubs"))
    results = {"params": dict(R=R, S=S, T=T, P=P, N=fm.number_of_nodes(), realizations=NUM_REALIZATIONS,
                              generations=GENERATIONS, alpha=0.1, tau=0.1), "runs": rows}
    with open("fm_results.json", "w") as fh:
        json.dump(results, fh)
    print(f"saved fm_results.json ({time.time() - start:.0f}s elapsed)")
