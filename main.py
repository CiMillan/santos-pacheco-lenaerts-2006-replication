"""Main simulation loop -- Santos, Pacheco & Lenaerts (2006).
Fixed across all network/update-rule choices; see network.py and
update_rule.py for the swappable pieces this loop calls into."""
import random

from network import build_network
from payoff import compute_payoffs
from update_rule import next_strategy


def run(network_kind, n, generations, R, S, T, P, seed, initial_c_fraction=0.5, m=4):
    rng = random.Random(seed)
    graph = build_network(network_kind, n, seed=seed, m=m)

    strategies = {node: ("C" if rng.random() < initial_c_fraction else "D") for node in graph.nodes}
    cooperation_trace = [sum(s == "C" for s in strategies.values()) / n]

    for _ in range(generations):
        payoffs = compute_payoffs(graph, strategies, R, S, T, P)
        strategies = {
            node: next_strategy(graph, node, strategies, payoffs, T, S, rng)
            for node in graph.nodes
        }
        cooperation_trace.append(sum(s == "C" for s in strategies.values()) / n)

    return cooperation_trace


def run_batch(network_kind, n, generations, R, S, T, P, num_realizations, seed, initial_c_fraction=0.5, m=4):
    """
    A single run() is noisy -- one random network, one random start. The
    paper reports results averaged over many independent realizations
    instead. This runs `num_realizations` fresh, independently-seeded
    simulations (seed, seed+1, seed+2, ...) and returns every trace, so the
    caller can average them.
    """
    return [
        run(network_kind, n, generations, R, S, T, P, seed + r, initial_c_fraction, m)
        for r in range(num_realizations)
    ]


def average_trace(traces):
    """Elementwise mean across realizations -- one trace in, same length as each input trace."""
    generations = len(traces[0])
    return [sum(trace[t] for trace in traces) / len(traces) for t in range(generations)]


if __name__ == "__main__":
    import json

    params = dict(network_kind="scale_free", n=1000, generations=200, R=1, S=-0.1, T=1.2, P=0,
                   num_realizations=100, seed=1)
    traces = run_batch(**params)
    avg = average_trace(traces)
    print(json.dumps({"params": params, "final_cooperation_fraction_avg": avg[-1], "avg_trace_tail": avg[-10:]}, indent=2))
