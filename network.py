"""Network generators -- Santos, Pacheco & Lenaerts (2006), Methods, p. 3493."""
import networkx as nx
import numpy as np


def build_network(kind, n, seed=None, m=4, avg_degree=8):
    """
    kind: one of the paper's four NoC types --
      "complete"          well-mixed limit, everyone connected to everyone.
      "scale_free"        Barabasi-Albert -- heavy-tailed degree distribution,
                           a few hub agents with many more links than most.
      "scale_free_random" same degree distribution as scale_free, but with
                           the age correlations between hubs removed by
                           repeated random edge-swapping (p. 3493: "randomly
                           and repeatedly exchanging the ends of pairs of
                           edges... washes out correlations without changing
                           the degree distribution").
      "single_scale"      moderate heterogeneity, Gaussian-tailed degree
                           distribution around avg_degree -- built via the
                           configuration model (p. 3493) on a Poisson degree
                           sequence, which is the standard fast-decaying-tail
                           stand-in for "single-scale" when the paper doesn't
                           give an exact generating distribution.
    n: number of agents.
    seed: RNG seed, for reproducibility.
    m: edges per new node in the Barabasi-Albert model (scale_free* only).
    avg_degree: target average degree for the single-scale network.
    """
    if kind == "complete":
        return nx.complete_graph(n)

    if kind == "scale_free":
        return nx.barabasi_albert_graph(n, m, seed=seed)

    if kind == "scale_free_random":
        g = nx.barabasi_albert_graph(n, m, seed=seed)
        nx.double_edge_swap(g, nswap=10 * g.number_of_edges(), max_tries=100 * g.number_of_edges(), seed=seed)
        return g

    if kind == "single_scale":
        rng = np.random.default_rng(seed)
        degrees = np.clip(rng.poisson(avg_degree, n), 1, None)
        if degrees.sum() % 2 != 0:
            degrees[0] += 1
        g = nx.Graph(nx.configuration_model(degrees, seed=seed))  # nx.Graph() collapses parallel edges
        g.remove_edges_from(nx.selfloop_edges(g))
        # A node whose entire stub budget went into a single self-loop ends
        # up with zero edges once that self-loop is removed above -- rare,
        # but real (more likely at low avg_degree, since a degree-2 node is
        # then more common). update_rule.py requires every node to have at
        # least one neighbor, so reconnect any such isolate to a random
        # other node rather than leaving it disconnected.
        isolates = list(nx.isolates(g))
        for node in isolates:
            other = rng.choice([v for v in g.nodes if v != node])
            g.add_edge(node, other)
        return g

    raise ValueError(f"unknown network kind: {kind}")
