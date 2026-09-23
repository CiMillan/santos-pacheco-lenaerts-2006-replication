"""Swarm main loop -- the swarm analogue of ../main.py's run()/run_batch().
Same structure (build network, loop generations of payoff -> update), so
results are comparable: both mechanisms see the same network, the same
payoff.py, and are recorded the same way."""
import random
import sys

sys.path.insert(0, "..")
from network import build_network
from payoff import compute_payoffs

from swarm_update_rule import next_position


def positions_to_strategies(positions):
    """Threshold each agent's continuous position at 0.5 to get the discrete
    C/D action actually played this generation (see ARCHITECTURE.txt)."""
    return {node: ("C" if p > 0.5 else "D") for node, p in positions.items()}


def run_swarm(network_kind, n, generations, R, S, T, P, seed, w=0.7, c1=1.5, c2=1.5, m=4, avg_degree=8):
    rng = random.Random(seed)
    graph = build_network(network_kind, n, seed=seed, m=m, avg_degree=avg_degree)

    positions = {node: rng.random() for node in graph.nodes}
    velocities = {node: 0.0 for node in graph.nodes}
    personal_best_position = dict(positions)
    personal_best_payoff = {node: float("-inf") for node in graph.nodes}

    cooperation_trace = [sum(s == "C" for s in positions_to_strategies(positions).values()) / n]

    for _ in range(generations):
        strategies = positions_to_strategies(positions)
        payoffs = compute_payoffs(graph, strategies, R, S, T, P)

        for node in graph.nodes:
            if payoffs[node] > personal_best_payoff[node]:
                personal_best_payoff[node] = payoffs[node]
                personal_best_position[node] = positions[node]

        updated = {
            node: next_position(graph, node, positions, velocities, personal_best_position, payoffs, w, c1, c2, rng)
            for node in graph.nodes
        }
        positions = {node: pos for node, (pos, vel) in updated.items()}
        velocities = {node: vel for node, (pos, vel) in updated.items()}

        cooperation_trace.append(sum(s == "C" for s in positions_to_strategies(positions).values()) / n)

    return cooperation_trace


def run_batch_swarm(network_kind, n, generations, R, S, T, P, num_realizations, seed, w=0.7, c1=1.5, c2=1.5, m=4, avg_degree=8):
    """Same purpose as ../main.py's run_batch(): num_realizations fresh,
    independently-seeded runs, so the caller can average them."""
    return [
        run_swarm(network_kind, n, generations, R, S, T, P, seed + r, w, c1, c2, m, avg_degree)
        for r in range(num_realizations)
    ]
