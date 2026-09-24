"""Main simulation loop with bots -- ../../main.py's loop, unchanged except for
three things: every agent gets a bot (bots.py), bots skip imitation, and
after imitation every bot makes one rewiring offer. ../../payoff.py and
../../update_rule.py are reused as-is. condition="none" adds no bots and is
exactly ../../main.py's run()."""
import random
import sys

sys.path.insert(0, "../..")
from network import build_network
from payoff import compute_payoffs
from update_rule import next_strategy

from bots import add_bots, bot_offer


def run(condition, network_kind, n, generations, R, S, T, P, seed, m=4, avg_degree=8):
    """
    condition: "none", "always_c", "random", "engaged" or "disengaged".
    Returns (cooperation_trace, degree_trace), each generations + 1 long:
      cooperation_trace -- fraction of AGENTS playing C (bots excluded);
      degree_trace      -- mean number of agent-agent ties per agent.
    """
    rng = random.Random(seed)
    graph = build_network(network_kind, n, seed=seed, m=m, avg_degree=avg_degree)
    agents = list(graph.nodes)

    strategies = {a: ("C" if rng.random() < 0.5 else "D") for a in agents}
    bots = [] if condition == "none" else add_bots(graph)
    strategies.update({b: "C" for b in bots})

    def cooperation():
        return sum(strategies[a] == "C" for a in agents) / n

    def mean_degree():
        return 2 * (graph.number_of_edges() - len(bots)) / n

    cooperation_trace, degree_trace = [cooperation()], [mean_degree()]

    for _ in range(generations):
        payoffs = compute_payoffs(graph, strategies, R, S, T, P)
        strategies.update({a: next_strategy(graph, a, strategies, payoffs, T, S, rng) for a in agents})
        if bots:
            cooperators = [a for a in agents if strategies[a] == "C"]
            for a in agents:
                bot_offer(graph, a, condition, strategies, cooperators, n, rng)
        cooperation_trace.append(cooperation())
        degree_trace.append(mean_degree())

    return cooperation_trace, degree_trace


def run_batch(condition, network_kind, n, generations, R, S, T, P, num_realizations, seed, m=4, avg_degree=8):
    """`num_realizations` independent runs, seeded seed, seed+1, ... like ../../main.py's run_batch()."""
    return [
        run(condition, network_kind, n, generations, R, S, T, P, seed + r, m, avg_degree)
        for r in range(num_realizations)
    ]
