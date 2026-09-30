"""Hybrid main loop -- the hybrid analogue of ../../main.py's run()/run_batch().
Same structure (build network, loop generations of payoff -> update), but
each node is either a human, who imitates with the paper's rule
(../../update_rule.py), or an AI agent, who learns from its own payoffs with
Q-learning (q_learning_rule.py). Both play the same game on the same network."""
import random
import sys

sys.path.insert(0, "../..")
from network import build_network
from payoff import compute_payoffs
from update_rule import next_strategy

from control_rules import fixed_action
from q_learning_rule import softmax_action, update_q


def assign_ai(graph, ai_fraction, placement, rng):
    """
    Picks which nodes are AI agents; the rest are humans.
    placement: "random" -- any nodes, chosen at random;
               "hubs"   -- the highest-degree nodes (ties broken by node id).
    Returns a set of AI node ids, of size round(ai_fraction * n).
    """
    k = round(ai_fraction * graph.number_of_nodes())
    nodes = sorted(graph.nodes)
    if placement == "random":
        return set(rng.sample(nodes, k))
    if placement == "hubs":
        return set(sorted(nodes, key=lambda v: -graph.degree[v])[:k])
    raise ValueError(f"unknown placement: {placement}")


def top_hubs(graph, share=0.05):
    """The top `share` of nodes by degree -- used only to record whether
    cooperators still hold the hubs, as Santos & Pacheco (2005) found."""
    k = max(1, round(share * graph.number_of_nodes()))
    return set(sorted(graph.nodes, key=lambda v: -graph.degree[v])[:k])


def fraction_c(strategies, nodes):
    """Share of cooperators among `nodes`; None if the group is empty."""
    nodes = list(nodes)
    if not nodes:
        return None
    return sum(strategies[v] == "C" for v in nodes) / len(nodes)


def run_hybrid(network_kind, n, generations, R, S, T, P, seed, ai_fraction, placement="random",
               alpha=0.1, tau=0.1, initial_c_fraction=0.5, m=4, avg_degree=8, ai_rule="q_learning"):
    """
    Returns {"all", "humans", "ai", "hubs"}: one cooperation trace each,
    one value per generation (generation 0 = the random start).
    AI reward = its payoff divided by its degree, i.e. the average payoff per
    game, so tau means the same thing for a hub and for a leaf
    (design choice, see ARCHITECTURE.txt). Humans use the raw accumulated
    payoff, exactly as in the paper.
    ai_rule: "q_learning" (default), or one of control_rules.CONTROL_RULES,
    stubborn AI agents that never learn, to test whether Q-learning matters.
    """
    rng = random.Random(seed)
    graph = build_network(network_kind, n, seed=seed, m=m, avg_degree=avg_degree)
    ai = assign_ai(graph, ai_fraction, placement, rng)
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


def run_batch_hybrid(network_kind, n, generations, R, S, T, P, num_realizations, seed, ai_fraction,
                     placement="random", alpha=0.1, tau=0.1, m=4, avg_degree=8, ai_rule="q_learning"):
    """Same purpose as ../../main.py's run_batch(): num_realizations fresh,
    independently-seeded runs (seed, seed+1, ...), so the caller can average them."""
    return [
        run_hybrid(network_kind, n, generations, R, S, T, P, seed + r, ai_fraction, placement,
                   alpha, tau, m=m, avg_degree=avg_degree, ai_rule=ai_rule)
        for r in range(num_realizations)
    ]
