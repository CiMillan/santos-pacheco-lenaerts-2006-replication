"""Main loop with Fermi humans -- ../extension-6-hybrid-population/main_hybrid.py's
run_hybrid() with one swap: humans imitate with fermi_rule.py (selection
pressure beta) instead of the Santos rule. AI agents, if any, are unchanged
(Q-learning). ai_fraction = 0 gives an all-human population."""
import random
import sys

sys.path.insert(0, "../..")
sys.path.insert(0, "../extension-6-hybrid-population")
from network import build_network
from payoff import compute_payoffs

from main_hybrid import assign_ai, fraction_c, top_hubs
from q_learning_rule import softmax_action, update_q

from fermi_rule import next_strategy_fermi


def run_fermi(network_kind, n, generations, R, S, T, P, seed, beta, ai_fraction=0.0,
              placement="hubs", alpha=0.1, tau=0.1, initial_c_fraction=0.5, m=4, avg_degree=8):
    """
    Returns {"all", "humans", "ai", "hubs"}: one cooperation trace each,
    one value per generation (generation 0 = the random start).
    Synchronous updates, as in our Santos replication (Pinheiro et al.
    update one random individual per time-step: design choice, no source).
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
            if node in ai:
                reward = payoffs[node] / graph.degree[node]
                q[node] = update_q(q[node], strategies[node], reward, alpha)
                new_strategies[node] = softmax_action(q[node], tau, rng)
            else:
                new_strategies[node] = next_strategy_fermi(graph, node, strategies, payoffs, beta, rng)
        strategies = new_strategies
        for name, g in groups.items():
            traces[name].append(fraction_c(strategies, g))

    return traces


def run_batch_fermi(network_kind, n, generations, R, S, T, P, num_realizations, seed, beta,
                    ai_fraction=0.0, placement="hubs", m=4, avg_degree=8):
    """num_realizations independently-seeded runs (seed, seed+1, ...)."""
    return [
        run_fermi(network_kind, n, generations, R, S, T, P, seed + r, beta, ai_fraction, placement,
                  m=m, avg_degree=avg_degree)
        for r in range(num_realizations)
    ]
