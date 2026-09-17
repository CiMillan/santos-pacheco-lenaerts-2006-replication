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
        return g

    raise ValueError(f"unknown network kind: {kind}")
