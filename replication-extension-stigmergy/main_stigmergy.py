"""Stigmergy main loop -- ../main.py's run()/run_batch(), unchanged except
for the traces: each generation, payoffs are computed, then every node's
trace is updated, then agents update by reading neighbours' traces
(stigmergy_update_rule.py). Traces start equal to the first generation's
payoffs, so they don't start from an artificial zero. trace_rule picks
update_traces ("average"), the update_traces_peak control ("peak"), or the
update_memory_peak control ("strategy"), where agents copy a neighbour's
REMEMBERED strategy instead of its current one. With lam=1 this is
exactly ../main.py's run(), same seed -> same trace."""
import random
import sys

sys.path.insert(0, "..")
from network import build_network
from payoff import compute_payoffs
from stigmergy_update_rule import next_strategy, update_traces, update_traces_peak, update_memory_peak

TRACE_RULES = {"average": update_traces, "peak": update_traces_peak}


def run_stigmergy(network_kind, n, generations, R, S, T, P, seed, lam, initial_c_fraction=0.5, m=4, avg_degree=8, trace_rule="average"):
    rng = random.Random(seed)
    graph = build_network(network_kind, n, seed=seed, m=m, avg_degree=avg_degree)

    strategies = {node: ("C" if rng.random() < initial_c_fraction else "D") for node in graph.nodes}
    cooperation_trace = [sum(s == "C" for s in strategies.values()) / n]
    traces, remembered = None, None

    for _ in range(generations):
        payoffs = compute_payoffs(graph, strategies, R, S, T, P)
        if traces is None:
            traces, remembered = dict(payoffs), dict(strategies)
        elif trace_rule == "strategy":
            traces, remembered = update_memory_peak(traces, remembered, payoffs, strategies, lam)
        else:
            traces = TRACE_RULES[trace_rule](traces, payoffs, lam)
        offered = remembered if trace_rule == "strategy" else strategies
        strategies = {
            node: next_strategy(graph, node, strategies, payoffs, traces, T, S, rng, offered)
            for node in graph.nodes
        }
        cooperation_trace.append(sum(s == "C" for s in strategies.values()) / n)

    return cooperation_trace


def run_batch_stigmergy(network_kind, n, generations, R, S, T, P, num_realizations, seed, lam, initial_c_fraction=0.5, m=4, avg_degree=8, trace_rule="average"):
    """Like ../main.py's run_batch(): seeds seed, seed+1, ... -> one trace each."""
    return [
        run_stigmergy(network_kind, n, generations, R, S, T, P, seed + r, lam, initial_c_fraction, m, avg_degree, trace_rule)
        for r in range(num_realizations)
    ]
