"""Hybrid main loop on the real FM network -- ../extension-6-hybrid-population/
main_hybrid.py's run_hybrid() with one swap: the network is given (the FM
giant component) instead of generated. Humans, AI agents, game and payoffs
are unchanged."""
import random
import sys

sys.path.insert(0, "../..")
sys.path.insert(0, "../extension-6-hybrid-population")
from payoff import compute_payoffs
from update_rule import next_strategy

from control_rules import fixed_action
from main_hybrid import assign_ai, fraction_c, top_hubs
from q_learning_rule import softmax_action, update_q


def pick_ai(graph, ai_fraction, placement, rng):
    """
    As extension 6's assign_ai(), plus one placement for the real network:
    "models" -- every node whose asset type is "model" are AI agents
    (ai_fraction is ignored). Design choice, no source.
    """
    if placement == "models":
        return {v for v, t in graph.nodes(data="type") if t == "model"}
    return assign_ai(graph, ai_fraction, placement, rng)


def run_hybrid_graph(graph, generations, R, S, T, P, seed, ai_fraction, placement="random",
                     alpha=0.1, tau=0.1, initial_c_fraction=0.5, ai_rule="q_learning"):
    """
    Returns {"all", "humans", "ai", "hubs"}: one cooperation trace each.
    The graph is fixed; the seed changes the starting strategies, the random
    AI placement and every random draw after that.
    """
    rng = random.Random(seed)
    ai = pick_ai(graph, ai_fraction, placement, rng)
    humans = set(graph.nodes) - ai
    hubs = top_hubs(graph)

    strategies = {node: ("C" if rng.random() < initial_c_fraction else "D") for node in graph.nodes}
    q = {node: {"C": 0.0, "D": 0.0} for node in ai}

    groups = {"all": graph.nodes, "humans": humans, "ai": ai, "hubs": hubs}
    traces = {name: [fraction_c(strategies, g)] for name, g in groups.items()}

    for _ in range(generations):
        payoffs = compute_payoffs(graph, strategies, R, S, T, P)
        new_strategies = {}
        for node in graph.nodes:
            if node in ai and ai_rule != "q_learning":
                new_strategies[node] = fixed_action(ai_rule, rng)
            elif node in ai:
                reward = payoffs[node] / graph.degree[node]
                q[node] = update_q(q[node], strategies[node], reward, alpha)
                new_strategies[node] = softmax_action(q[node], tau, rng)
            else:
                new_strategies[node] = next_strategy(graph, node, strategies, payoffs, T, S, rng)
        strategies = new_strategies
        for name, g in groups.items():
            traces[name].append(fraction_c(strategies, g))

    return traces


def run_batch_graph(graph, generations, R, S, T, P, num_realizations, seed, ai_fraction,
                    placement="random", ai_rule="q_learning"):
    """num_realizations independently-seeded runs (seed, seed+1, ...) on the same graph."""
    return [run_hybrid_graph(graph, generations, R, S, T, P, seed + r, ai_fraction, placement,
                             ai_rule=ai_rule)
            for r in range(num_realizations)]
