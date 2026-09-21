"""Payoff accumulation -- Santos, Pacheco & Lenaerts (2006), Methods, p. 3493.
Each agent plays every graph neighbor once per generation; payoffs accumulate."""

OUTCOME = {("C", "C"): "R", ("C", "D"): "S", ("D", "C"): "T", ("D", "D"): "P"}


def compute_payoffs(graph, strategies, R, S, T, P):
    """
    graph: networkx Graph.
    strategies: dict {node: "C" or "D"}.
    Returns dict {node: accumulated payoff this generation}.
    """
    matrix = {"R": R, "S": S, "T": T, "P": P}
    payoff = {node: 0.0 for node in graph.nodes}
    for x, y in graph.edges:
        payoff[x] += matrix[OUTCOME[(strategies[x], strategies[y])]]
        payoff[y] += matrix[OUTCOME[(strategies[y], strategies[x])]]
    return payoff
