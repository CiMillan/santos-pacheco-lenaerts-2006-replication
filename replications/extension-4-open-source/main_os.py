"""Main simulation loop with programs -- ../../main.py's loop, unchanged except
for three things: agents start with a random program (1/5 each) instead of
C/D, payoffs come from payoff_os.py, and cooperation is measured per
meeting. ../../update_rule.py's next_strategy() is reused as-is: it copies a
neighbour's label, and a program name is just a label."""
import random
import sys

sys.path.insert(0, "../..")
from network import build_network
from update_rule import next_strategy

from programs import PROGRAMS
from payoff_os import compute_payoffs, cooperation_fraction


def program_shares(programs):
    """Fraction of agents running each program: {program name: share}."""
    n = len(programs)
    return {p: sum(q == p for q in programs.values()) / n for p in PROGRAMS}


def run(network_kind, n, generations, R, S, T, P, seed, m=4, avg_degree=8, cost=0.0):
    """
    Returns (cooperation_trace, final program shares). cooperation_trace
    has generations + 1 entries (the start, then one per generation), like
    ../../main.py's run(). cost: per-game proof cost, see payoff_os.py.
    """
    rng = random.Random(seed)
    graph = build_network(network_kind, n, seed=seed, m=m, avg_degree=avg_degree)

    programs = {node: rng.choice(PROGRAMS) for node in graph.nodes}
    cooperation_trace = [cooperation_fraction(graph, programs)]

    for _ in range(generations):
        payoffs = compute_payoffs(graph, programs, R, S, T, P, cost)
        programs = {
            node: next_strategy(graph, node, programs, payoffs, T, S, rng)
            for node in graph.nodes
        }
        cooperation_trace.append(cooperation_fraction(graph, programs))

    return cooperation_trace, program_shares(programs)


def run_batch(network_kind, n, generations, R, S, T, P, num_realizations, seed, m=4, avg_degree=8, cost=0.0):
    """`num_realizations` independent runs, seeded seed, seed+1, ... like ../../main.py's run_batch()."""
    return [
        run(network_kind, n, generations, R, S, T, P, seed + r, m, avg_degree, cost)
        for r in range(num_realizations)
    ]
